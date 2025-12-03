# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
    # الداشبورد الجديد
    path('', views.dashboard_redirect, name='dashboard'),                    # /accounts/
    path('investor/', views.investor_dashboard, name='investor_dashboard'), # /accounts/investor/
    path('owner/', views.owner_dashboard, name='owner_dashboard'),          # /accounts/owner/
    path('admin/', views.admin_dashboard, name='admin_dashboard'),         # /accounts/admin/
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
]