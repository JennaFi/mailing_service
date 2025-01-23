from datetime import datetime

from django.db import models

from users.models import User


class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Recipient email')
    name = models.CharField(max_length=255, verbose_name='Recipient name')
    comment = models.TextField(max_length=255, verbose_name='Comment', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipients',
                              verbose_name='Owner',
                              )

    def __str__(self):
        return f'{self.name} <{self.email}>'

    class Meta:
        verbose_name = 'Recipient'
        verbose_name_plural = 'Recipients'
        ordering = ['id']


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Title')
    message = models.TextField(verbose_name='Text message')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages',
                              verbose_name='Owner',
                              )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['id']


class Mailing(models.Model):
    COMPLETED = 'completed'
    CREATED = 'created'
    RUNNING = 'running'

    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (CREATED, 'Created'),
        (RUNNING, 'Running'),
    ]

    first_send_at = models.DateTimeField(default=datetime.now(), verbose_name='Date and time to start', )
    finish_send_at = models.DateTimeField(default=datetime.now(), verbose_name='Date and time to finish')
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CREATED, verbose_name='Status')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True, related_name='Mailing',
                                verbose_name='Message')

    recipients = models.ManyToManyField(Recipient, related_name='Mailing', verbose_name='Recipients')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mailings',
                              verbose_name='Owner', )
    is_disabled = models.BooleanField(default=False, verbose_name='disabled')

    def __str__(self):
        amount = self.recipients.count()
        return f'Mail {self.pk}, Title: {self.message.title}, amount of recipients: {amount}'

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
        ordering = ['-id']
        permissions = [
            ('can_disable_mailing', 'Can_disable_mailing'),
        ]


class MailingAttempts(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUS_CHOICES = [
        (SUCCESS, 'Success'),
        (FAILURE, 'Failure'),
    ]

    attempted_at = models.DateTimeField(verbose_name='Date and time of attempt', )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='SUCCESS', verbose_name='Status')

    mail_server_response = models.TextField(
        null=True,
        blank=True,
        verbose_name='Server response',
    )

    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name='Mailing',
    )

    def __str__(self):
        return f'Attempt {self.pk}, State: {self.status}, {self.attempted_at}'

    class Meta:
        verbose_name = 'Mailing attempt'
        verbose_name_plural = 'Mailing attempts'
        ordering = ['-attempted_at']
