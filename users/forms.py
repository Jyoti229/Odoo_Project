from django import forms
from .models import CustomUser

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role', 'first_name', 'last_name']


# OTP Verification Form
class OTPVerificationForm(forms.Form):
    email = forms.EmailField()
    otp = forms.CharField(max_length=6)
