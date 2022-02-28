from django.urls import path

from .views import (LoginView, ProfileView, RegisterView,
                    ForgotPasswordView, NewPasswordView,
                    LogoutView, VerificationView, VerifyPasswordChange)

app_name = 'accounts'
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('signup', RegisterView.as_view(), name='register'),
    path('verification/<uidb64>/<token>', VerificationView.as_view(), name='verify'),
    path('forgot_password', ForgotPasswordView.as_view(),
         name='forgot_password'),
    path('verify_password_change/<uidb64>/<token>', VerifyPasswordChange.as_view(), name='verify_password_change'),
    path('new_password', NewPasswordView.as_view(), name='new_password'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('logout', LogoutView.as_view(), name='logout'),
]
