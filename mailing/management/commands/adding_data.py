from django.core.management import call_command
from django.core.management.base import BaseCommand

from mailing.models import Mailing, MailingAttempts, Message, Recipient


class Command(BaseCommand):
    help = 'Adding data from fixtures'

    def handle(self, *args, **kwargs):
        Recipient.objects.all().delete()
        Message.objects.all().delete()
        Mailing.objects.all().delete()
        MailingAttempts.objects.all().delete()

        call_command('', 'recipients_fixture.json', format='json')
        self.stdout.write(self.style.SUCCESS('Recipients successfully added'))
        call_command('loaddata', 'messages_fixture.json', format='json')
        self.stdout.write(self.style.SUCCESS('Messages successfully added'))
        call_command('loaddata', 'mailing_fixture.json', format='json')
        self.stdout.write(self.style.SUCCESS('Mailing successfully added'))
        call_command('loaddata', 'mailing_attempts_fixture.json', format='json')
        self.stdout.write(self.style.SUCCESS('Mailing attempts successfully added'))
