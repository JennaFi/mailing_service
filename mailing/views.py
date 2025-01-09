from datetime import datetime
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView

from mailing.forms import RecipientsForm, MessageForm, MailingForm
from mailing.models import Recipient, Message, Mailing, MailingAttempts


class MainView(TemplateView):
    template_name = 'mailing/main_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients_count'] = Recipient.objects.count()
        context['messages_count'] = Message.objects.count()
        context['mailings_count'] = Mailing.objects.count()
        context['attempts_count'] = MailingAttempts.objects.count()
        context['attempts'] = MailingAttempts.objects.all()[:10]
        context['attempt_success_count'] = MailingAttempts.objects.filter(status='success').count()
        context['attempt_failure_count'] = MailingAttempts.objects.filter(status='failure').count()

        return context


class RecipientListView(ListView):
    model = Recipient
    context_object_name = 'recipients'
    template_name = 'mailing/recipient_list.html'

    def get_queryset(self):
        return Recipient.objects.all().order_by('name')


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientsForm
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientUpdateView(UpdateView, LoginRequiredMixin):
    model = Recipient
    form_class = RecipientsForm
    success_url = reverse_lazy('mailing:recipient_list')


class RecipientDeleteView(DeleteView, LoginRequiredMixin):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')


class MessageListView(ListView):
    model = Message
    context_object_name = 'messages'
    template_name = 'mailing/message_list.html'


class MessageCreateView(CreateView):
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


class MailingListView(ListView):
    model = Mailing

    def get_queryset(self):
        queryset = Mailing.objects.prefetch_related('recipients')
        return queryset


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

    def get_queryset(self):
        queryset = Mailing.objects.prefetch_related('recipients')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipients'] = self.object.recipients.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        subject = self.object.message
        message = self.object.message.message
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


class MailingAttemptsListView(ListView):
    model = MailingAttempts
