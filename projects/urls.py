# projects/urls.py
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='list'),
    path('create/', views.project_create, name='create'),
    path('<int:pk>/', views.project_detail, name='detail'),
    path('<int:pk>/invest/', views.invest_in_project, name='invest'),
    path('<int:project_id>/payment/', views.payment_page, name='payment'),  # ← جديد
]