from django.urls import path
from . import views
from .views_home import home_view

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('signup/', views.signup_view, name='signup'),
    path('otp-verify/', views.otp_verify_view, name='otp_verify'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', home_view, name='home'),
]
