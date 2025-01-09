import secrets

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetCompleteView
from django.core.checks import messages
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView

from mailing_service.settings import DEFAULT_FROM_EMAIL
from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class UserListView(LoginRequiredMixin, ListView):
    model = User

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden(
            "You don't have permission to view or change or delete this user"
        )


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('mailing:main_page')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}/"
        send_mail(subject='Подтверждение почты',
                  message=f"Добро пожалдовать в систему! Перейди, пожалуйста, по ссылке для подтверждения почты {url}",
                  from_email=DEFAULT_FROM_EMAIL,
                  recipient_list=[user.email],
                  )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('user:login'))


class UserUpdateProfile(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/profile_update.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Profile updated successfully')
        return redirect(reverse('users:edit_profile'))

    def form_invalid(self, form):
        messages.error(self.request, 'Profile update failed')
        return redirect(reverse('users:edit_profile'))


class UserBlockView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if not request.user.has_perm('users.can_block_user'):
            return HttpResponseForbidden('You do not have permission to block this user')

        user.is_active = not user.is_active
        user.save()

        return redirect('users:users')
