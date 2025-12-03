# pages/views.py
from django.shortcuts import render

def home(request):
    # نجيب آخر 6 مشاريع منشورة عشان نعرضهم في الصفحة الرئيسية
    from projects.models import Project
    latest_projects = Project.objects.filter(is_approved=True).order_by('-created_at')[:6]
    
    return render(request, 'pages/home.html', {
        'latest_projects': latest_projects
    })

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')