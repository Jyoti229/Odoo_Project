from django.shortcuts import render, redirect
from .forms import SignupForm, OTPVerificationForm
from .models import CustomUser, OTP
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
import random
import datetime

def signup_view(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.is_active = False  # Inactive until OTP verified
			user.save()

			# Generate 6-digit OTP
			otp_code = f"{random.randint(100000, 999999)}"
			expires_at = timezone.now() + datetime.timedelta(minutes=10)
			OTP.objects.create(user=user, code=otp_code, expires_at=expires_at)

			# Send OTP via email (console backend for dev)
			send_mail(
				'Your OTP Code',
				f'Your OTP code is: {otp_code}',
				'noreply@rental.com',
				[user.email],
				fail_silently=False,
			)

			messages.success(request, 'Account created! Please check your email for OTP.')
			return redirect('login')
	else:
		form = SignupForm()
	return render(request, 'users/signup.html', {'form': form})


# OTP Verification View
def otp_verify_view(request):
	if request.method == 'POST':
		form = OTPVerificationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			otp_code = form.cleaned_data['otp']
			try:
				user = CustomUser.objects.get(email=email)
				otp_obj = OTP.objects.filter(user=user, code=otp_code, is_used=False).last()
				if otp_obj and not otp_obj.is_expired():
					user.is_active = True
					user.save()
					otp_obj.is_used = True
					otp_obj.save()
					messages.success(request, 'OTP verified! You can now log in.')
					return redirect('login')
				else:
					messages.error(request, 'Invalid or expired OTP.')
			except CustomUser.DoesNotExist:
				messages.error(request, 'User not found.')
	else:
		form = OTPVerificationForm()
	return render(request, 'users/otp_verify.html', {'form': form})


# Login View
def login_view(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(request, email=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.success(request, 'Logged in successfully!')
				return redirect('home')  # Change to your home/dashboard view
			else:
				messages.error(request, 'Account not active. Please verify OTP.')
		else:
			messages.error(request, 'Invalid credentials.')
	return render(request, 'users/login.html')

# Logout View
def logout_view(request):
	logout(request)
	messages.success(request, 'Logged out successfully!')
	return redirect('login')
