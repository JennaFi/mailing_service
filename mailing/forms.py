from django import forms

from mailing.models import Mailing, Recipient, Message


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = [
            'owner',
        ]
        widgets = {
            'recipients': forms.CheckboxSelectMultiple(),
        }


class MailingManagerForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('is_disabled',)
        widgets = {
            'is_disabled': forms.CheckboxInput(),
        }
        labels = {
            'is_disabled': 'Disable mailing',
        }


class RecipientsForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'
        exclude = [
            'owner',
        ]


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = [
            'owner',
        ]
