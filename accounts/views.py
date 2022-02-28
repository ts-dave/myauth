from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.views import View

from .forms import SignupForm, LoginForm, PasswordChangeForm
from .mixins import LogoutRequiredMixin
from .tokens import token_generator
from accounts.models import User


class LoginView(LogoutRequiredMixin, View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # TODO: Handle remember_me
                return redirect('accounts:profile')

            else:
                try:
                    user = get_user_model().objects.get(username=username)

                    if not user.is_active:
                        domain = get_current_site(request).domain
                        relative_url = reverse('accounts:verify', kwargs={
                            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': token_generator.make_token(user),
                        })
                        body = f'Click on link or copy into your browser to verify email: {domain}{relative_url}'

                        msg = EmailMessage(
                            'Myauth: Email Verification',
                            body,
                            settings.DEFAULT_FROM_MAIL,
                            [user.email],
                        )
                        msg.send(fail_silently=False)

                        messages.success(request, 'Check inbox to verify email')
                        return redirect('accounts:login')

                except get_user_model().DoesNotExist:
                    messages.error(request, 'Invalid username or password')
                    return redirect('accounts:login')

        messages.error(request, 'Invalid credentials')
        return redirect('accounts:login')


class RegisterView(LogoutRequiredMixin, View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = get_user_model().objects.create_user(username=username, email=email,
                                                        password=password, is_active=False)
            user.save()

            domain = get_current_site(request).domain
            relative_url = reverse('accounts:verify', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            body = f'Click on link or copy into your browser to verify email: {domain}{relative_url}'

            msg = EmailMessage(
                'Myauth: Email Verification',
                body,
                settings.DEFAULT_FROM_MAIL,
                [email],
            )
            msg.send(fail_silently=False)

            messages.success(request, 'Profile Created! Check inbox to verify email')
            return redirect('accounts:login')

        messages.error(request, 'Details Invalid! Try again')
        return render(request, 'register.html', {'form': form})


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=user_id)

            if token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                messages.success(request, 'Verification Successful! Please login')
                return redirect('accounts:login')

            else:
                messages.error(request, 'Invalid token! ')
                return redirect('accounts:register')

        except Exception as e:
            messages.error(request, 'Verificatoion error')
            return redirect('accounts:register')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'profile.html')


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'password_reset.html')

    def post(self, request):
        email = request.POST['email']

        try:
            user = get_user_model().objects.get(email=email)
            domain = get_current_site(request).domain
            relative_url = reverse('accounts:verify_password_change', kwargs={
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            body = f'Click link or copy into your browser to verify password reset token: {domain}{relative_url}'
            msg = EmailMessage(
                'Myauth: Password Reset Verification',
                body,
                settings.DEFAULT_FROM_MAIL,
                [email],
            )
            msg.send(fail_silently=False)

            messages.success(request, "Check your inbox to verify email")
            return redirect('accounts:forgot_password')

        except get_user_model().DoesNotExist:
            messages.error(request, 'Email not recognized')
            return redirect('accounts:forgot_password')


class VerifyPasswordChange(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=user_id)

            if default_token_generator.check_token(user, token):
                login(request, user)
                return redirect('accounts:new_password')

            else:
                messages.error(request, 'Invalid token! ')
                return redirect('accounts:forgot_password')

        except Exception as e:
            messages.error(request, 'Verificatoion error')
            return redirect('accounts:forgot_password')


class NewPasswordView(View):
    def get(self, request):
        form = PasswordChangeForm()
        return render(request, 'new_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(request.POST)

        if form.is_valid():
            new_password = form.cleaned_data['password1']
            user = get_user_model().objects.get(username=request.user.username)
            user.set_password(new_password)
            user.save()

            messages.success(request, "Password reset successful")
            return redirect('accounts:login')

        messages.error(request, 'Invalid Entries')
        return render(request, 'new_password.html', {'form': form})


class LogoutView(LoginRequiredMixin, View):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')
