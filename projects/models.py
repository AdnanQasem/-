# projects/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان المشروع")
    description = models.TextField(verbose_name="وصف المشروع")
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="المبلغ المطلوب")
    raised_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="المبلغ المجموع")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects', verbose_name="صاحب المشروع")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    is_approved = models.BooleanField(default=False, verbose_name="موافق عليه")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="صورة المشروع")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "مشروع"
        verbose_name_plural = "المشاريع"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:detail', args=[self.id])

    def progress(self):
        return (self.raised_amount / self.goal_amount) * 100 if self.goal_amount > 0 else 0


class Investment(models.Model):
    investor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="المبلغ المستثمر")
    invested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-invested_at']

    def __str__(self):
        return f"{self.investor} استثمر {self.amount} في {self.project}"
