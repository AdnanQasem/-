from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ('INVESTOR', 'Investor'),  # مستثمر
        ('OWNER', 'Owner'),        # صاحب مشروع
    )
    
    # 👇 حقل الصورة
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='INVESTOR')
    phone = models.CharField(max_length=20, blank=True)
    # معلومات اختيارية:
    city = models.CharField(max_length=80, blank=True)
    bio  = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)  # للتحقق من البريد لاحقًا

    def __str__(self):
        return f"{self.user.username} ({self.role})"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()