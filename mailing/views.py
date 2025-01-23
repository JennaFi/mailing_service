from datetime import datetime

from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from mailing.forms import RecipientsForm, MessageForm, MailingForm, MailingManagerForm
from mailing.models import Recipient, Message, Mailing, MailingAttempts
from mailing.services import get_context_from_cash
from users.models import User


class MainView(TemplateView):
    template_name = 'mailing/main_page.html'

    def get_context_data(self, **kwargs):
        user = self.request.user

        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().filter().distinct().count()
        context['recipients_count'] = Recipient.objects.count()
        context['messages_count'] = Message.objects.count()
        context['mailings_count'] = Mailing.objects.filter(is_disabled=False).distinct().count()
        context['attempts_count'] = MailingAttempts.objects.count()
        context['attempts'] = MailingAttempts.objects.all()[:10]
        context['attempt_success_count'] = MailingAttempts.objects.filter(status='success').count()
        context['attempt_failure_count'] = MailingAttempts.objects.filter(status='failure').count()
        context['mailings_running_count'] = Mailing.objects.filter(status='running').count()

        context.update(get_context_from_cash(user))

        return context


class UserMailingView(TemplateView, LoginRequiredMixin):
    template_name = 'mailing/user_mailing.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        user_mailings = Mailing.objects.filter(owner=user)

        successful_attempts = MailingAttempts.objects.filter(mailing__in=user_mailings,
                                                             status=MailingAttempts.SUCCESS).count()

        failed_attempts = MailingAttempts.objects.filter(mailing__in=user_mailings,
                                                         status=MailingAttempts.FAILURE).count()

        context.update({
            'mailings_count': user_mailings.count(),
            'successful_attempts': successful_attempts,
            'failed_attempts': failed_attempts,
        })

        return context


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    context_object_name = 'recipients'
    template_name = 'mailing/recipient_list.html'

    def get_queryset(self):
        user = self.request.user
        user_mailings = Mailing.objects.filter(owner=user)
        recipients = Recipient.objects.filter(Mailing__in=user_mailings).distinct()
        return recipients.order_by('name')


class RecipientCreateView(CreateView, LoginRequiredMixin):
    model = Recipient
    form_class = RecipientsForm
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientUpdateView(UpdateView, LoginRequiredMixin):
    model = Recipient
    form_class = RecipientsForm

    success_url = reverse_lazy('mailing:recipient_list')


class RecipientDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')


class MessageListView(ListView, LoginRequiredMixin):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message_list.html'

    def get_queryset(self):
        user = self.request.user
        user_mailings = Mailing.objects.filter(owner=user)
        messages = Message.objects.filter(Mailing__in=user_mailings).distinct()
        return messages.order_by('title')


class MessageCreateView(CreateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageUpdateView(UpdateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_list')


class MessageDeleteView(DeleteView, LoginRequiredMixin):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingListView(ListView, LoginRequiredMixin):
    model = Mailing

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('mailing.can_disable_mailing'):
            return Mailing.objects.all()

        return Mailing.objects.filter(owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_manager = self.request.user.has_perm('mailing.can_disable_mailing')

        context['is_manager'] = is_manager
        return context


class MailingCreateView(CreateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user

        if user == self.object.owner:
            return MailingForm
        if user.has_perm('mailing.can_disable_mailing'):
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(DetailView, LoginRequiredMixin):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        subject = self.object.message
        message = self.object.message
        from_email = 'eva.oww@gmail.com'
        recipient_list = [
            recipient.email for recipient in self.object.recipients.all()
        ]

        for recipient in recipient_list:
            try:
                send_mail(subject, message, from_email, [recipient])
                response = f"{recipient}: Success"
                MailingAttempts.objects.create(
                    attempted_at=timezone.now(),
                    status='success',
                    mail_server_response=response,
                    mailing=self.object,
                )

            except Exception as e:
                response = f"{recipient}: Error: {str(e)}"

                MailingAttempts.objects.create(
                    attempted_at=datetime.now(),
                    status='failure',
                    mail_server_response=response,
                    mailing=self.object,
                )

        return redirect('mailing:mailing_list')


class MailingAttemptsListView(ListView, LoginRequiredMixin):
    model = MailingAttempts
