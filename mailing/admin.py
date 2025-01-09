from django.contrib import admin

from mailing.models import Message, Recipient, Mailing, MailingAttempts

admin.site.register(Message)

admin.site.register(MailingAttempts)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_send_at',
        'finish_send_at',
        'status',
        'message',
        'get_recipients',
    )
    list_filter = ('status', 'message')
    search_fields = ('message__title', 'recipients__name', 'recipients__email')

    def get_recipients(self, obj):
        return ', '.join([f'{rec.name} <{rec.email}>' for rec in obj.recipients.all()])

    get_recipients.short_description = 'Recipients'


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'comment')
    search_fields = ('name', 'email')
    list_filter = ('name',)
