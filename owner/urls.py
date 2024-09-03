from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,AccessRefreshView,OTPRequestView, OTPVerificationView,PasswordResetView
from . import views

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('refresh', AccessRefreshView.as_view()),
    path('logout', LogoutView.as_view()),
    path('test',views.testget),
    path('request_otp', OTPRequestView.as_view()),
    path('verify_otp', OTPVerificationView.as_view() ),
    path('reset_password', PasswordResetView.as_view()),

]