# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from .forms import RegisterForm, LoginForm, ProfileUpdateForm
from .models import Profile
from projects.models import Project, Investment  # ← مهم جدًا (هنستخدمهم في الداشبورد)
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileUpdateForm

# ====================== التسجيل والدخول ======================
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            role = form.cleaned_data['role']
            avatar = request.FILES.get('avatar')

    # نعمل المستخدم
            user = User.objects.create_user(username=username, email=email, password=password)

    # نعمل البروفايل بطريقة آمنة (ما تطلع أبدًا UNIQUE error)
            Profile.objects.update_or_create(
                user=user,
                defaults={'role': role,
                'avatar': avatar  # 👈 هي المهمة
}

            )

            messages.success(request, "تم إنشاء الحساب بنجاح، يمكنك تسجيل الدخول الآن.")
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ← السطرين دول هما اللي بيحلوا المشكلة نهائيًا
            update_session_auth_hash(request, user)   # يحدّث الـ CSRF token بدون ما يخرّجك
            request.session.modified = True           # يضمن تحديث الجلسة

            messages.success(request, "تم تسجيل الدخول بنجاح!")
            return redirect('accounts:dashboard')
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "تم تسجيل الخروج بنجاح.")
    return redirect('home')


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تحديث الملف الشخصي بنجاح.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "accounts/profile.html", {"form": form})


# ====================== الداشبورد حسب الدور ======================
@login_required
def dashboard_redirect(request):
    """يوجه المستخدم للداشبورد المناسب حسب دوره"""
    role = request.user.profile.role
    if role == 'INVESTOR':
        return redirect('accounts:investor_dashboard')
    elif role == 'OWNER':
        return redirect('accounts:owner_dashboard')
    else:
        return redirect('accounts:admin_dashboard')


@login_required
def investor_dashboard(request):
    if request.user.profile.role != 'INVESTOR':
        return redirect('accounts:dashboard')
    
    investments = Investment.objects.filter(investor=request.user).select_related('project')
    total_invested = investments.aggregate(total=Sum('amount'))['total'] or 0

    return render(request, 'accounts/investor_dashboard.html', {
        'investments': investments,
        'total_invested': total_invested,
    })



@login_required
def owner_dashboard(request):
    if request.user.profile.role != 'OWNER':
        return redirect('accounts:dashboard')
    
    my_projects = Project.objects.filter(owner=request.user)

    return render(request, 'accounts/owner_dashboard.html', {
        'my_projects': my_projects,
    })


@login_required
def admin_dashboard(request):
    # لو بدك تحدد دور المشرف باسم معين، غيّر الشرط
    if request.user.profile.role not in ['ADMIN', 'admin']:
        return redirect('accounts:dashboard')
    
    context = {
        'total_users': User.objects.count(),
        'total_projects': Project.objects.count(),
        'pending_projects': Project.objects.filter(is_approved=False).count(),
        'total_investments': Investment.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context)

@login_required
def profile_edit(request):
    profile = request.user.profile  # نأكد إن الـ profile موجود

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # حفظ الاسم الأول والأخير في الـ User
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.save()

            form.save()
            return redirect('accounts:profile')
    else:
        # ننشئ الفورم ونملي الحقول يدويًا بأمان
        form = ProfileUpdateForm(instance=profile)
        form.initial['first_name'] = request.user.first_name
        form.initial['last_name'] = request.user.last_name

    return render(request, 'accounts/profile_edit.html', {'form': form})