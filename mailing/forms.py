from django import forms

from mailing.models import Mailing, Recipient, Message


class MailingForm(forms.Form):
    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = [
            'owner',
        ]
        widgets = {
            'recipients': forms.CheckboxSelectMultiple(),
        }

class RecipientsForm(forms.Form):

    class Meta:
        model = Recipient
        fields = '__all__'
        exclude = [
            'owner',
        ]

class MessageForm(forms.Form):

    class Meta:
        model = Message
        fields = '__all__'
        exclude = [
            'owner',
        ]