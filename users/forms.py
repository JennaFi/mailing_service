from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, BooleanField

from users.models import User


class StyleFirmMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label


class UserRegisterForm(StyleFirmMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserUpdateForm(StyleFirmMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ['email']

