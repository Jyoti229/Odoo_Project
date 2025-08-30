from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
	def create_user(self, email, password=None, **extra_fields):
		if not email:
			raise ValueError('The Email field must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
	ROLE_CHOICES = (
		('customer', 'Customer'),
		('admin', 'Admin'),
	)
	username = None  # Remove username field
	email = models.EmailField(unique=True)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email

	# OTP Model for email verification
from django.utils import timezone
import datetime

class OTP(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	code = models.CharField(max_length=6)
	created_at = models.DateTimeField(auto_now_add=True)
	expires_at = models.DateTimeField()
	is_used = models.BooleanField(default=False)

	def is_expired(self):
		return timezone.now() > self.expires_at

	def __str__(self):
		return f"OTP for {self.user.email}: {self.code}"
