# projects/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Project, Investment



def payment_page(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'projects/payment.html', {'project': project})
# قائمة المشاريع المنشورة فقط (للجميع حتى غير المسجلين)
def project_list(request):
    projects = Project.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'projects/project_list.html', {'projects': projects})

# تفاصيل المشروع
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk, is_approved=True)
    investments = project.investments.all().order_by('-invested_at')
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'investments': investments
    })

# إضافة مشروع جديد (للـ OWNER فقط)
@login_required
def project_create(request):
    if request.user.profile.role != 'OWNER':
        messages.error(request, 'فقط أصحاب المشاريع يمكنهم إضافة مشروع!')
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        goal_amount = request.POST['goal_amount']
        image = request.FILES.get('image')

        project = Project.objects.create(
            title=title,
            description=description,
            goal_amount=goal_amount,
            owner=request.user,
            image=image
        )
        messages.success(request, 'تم إرسال المشروع للمراجعة بنجاح! سيتم نشره بعد الموافقة.')
        return redirect('projects:list')

    return render(request, 'projects/project_create.html')

# استثمار في مشروع
@login_required
def invest_in_project(request, pk):
    project = get_object_or_404(Project, pk=pk, is_approved=True)
    
    if request.user.profile.role != 'INVESTOR':
        messages.error(request, 'فقط المستثمرين يمكنهم الاستثمار!')
        return redirect('projects:detail', pk=pk)

    if request.method == 'POST':
        try:
            amount = float(request.POST['amount'])
            if amount <= 0:
                raise ValueError
        except:
            messages.error(request, 'أدخل مبلغ صحيح!')
            return redirect('projects:detail', pk=pk)

        # نضيف الاستثمار
        Investment.objects.create(
            investor=request.user,
            project=project,
            amount=amount
        )
        # نحدّث المبلغ المجموع
        project.raised_amount += amount
        project.save()

        messages.success(request, f'تم استثمار {amount} ₪ بنجاح في المشروع!')
        return redirect('projects:detail', pk=pk)

    return redirect('projects:detail', pk=pk)