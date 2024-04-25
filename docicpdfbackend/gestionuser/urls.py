from django.urls import path
from django.urls.conf import include
from django.views.generic import RedirectView, TemplateView

from .views import RegisterView, VerifyEmail, UserLoginAPIView, UserChangePasswordView, \
    UserProfileView, UserLogoutView, ConfirmResetPasswordView, PasswordResetRequestView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-veriify'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path( 'password-reset-confirm/<uidb64>/<token>/', ConfirmResetPasswordView.as_view(), name='confirmepwd' ),

    path('change-password/', UserChangePasswordView.as_view(), name='change-password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path( 'logout/', UserLogoutView.as_view(), name='logout' ),


]
