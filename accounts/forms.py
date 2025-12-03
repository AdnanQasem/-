from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label="كلمة المرور", widget=forms.PasswordInput)
    password2 = forms.CharField(label="تأكيد كلمة المرور", widget=forms.PasswordInput)

    ROLE_CHOICES = Profile.ROLE_CHOICES
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="نوع الحساب")

    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("كلمتا المرور غير متطابقتين")
        return password2

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="اسم المستخدم أو البريد الإلكتروني",
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control'})
    )
    password = forms.CharField(
        label="كلمة المرور",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'city', 'bio']
        labels = {
            'phone': 'رقم الهاتف',
            'city': 'المدينة',
            'bio': 'نبذة عنك',
        }