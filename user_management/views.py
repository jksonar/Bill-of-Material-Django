from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'user_management/register.html'
    success_url = reverse_lazy('user_management:login')

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user_management/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'user_management/edit_profile.html'
    success_url = reverse_lazy('user_management:profile')

    def get_object(self):
        return self.request.user

class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'user_management/password_change.html'
    success_url = reverse_lazy('user_management:password_change_done')

class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'user_management/password_change_done.html'

class PasswordResetView(PasswordResetView):
    template_name = 'user_management/password_reset.html'
    email_template_name = 'user_management/password_reset_email.html'
    success_url = reverse_lazy('user_management:password_reset_done')

class PasswordResetDoneView(PasswordResetDoneView):
    template_name = 'user_management/password_reset_done.html'

class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user_management/password_reset_confirm.html'
    success_url = reverse_lazy('user_management:password_reset_complete')

class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'user_management/password_reset_complete.html'
