from django.contrib import admin

# Register your models here.
# projects/admin.py
from django.contrib import admin
from .models import Project, Investment

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'goal_amount', 'raised_amount', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['title', 'description']
    actions = ['approve_projects']

    def approve_projects(self, request, queryset):
        queryset.update(is_approved=True)
    approve_projects.short_description = "موافقة على المشاريع المختارة"


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['investor', 'project', 'amount', 'invested_at']
    list_filter = ['invested_at']