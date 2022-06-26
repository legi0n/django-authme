from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm as BaseAuthenticationForm

__all__ = [
    'RegistrationForm',
    'AuthenticationForm',
]


User = get_user_model()


class RegistrationForm(UserCreationForm):
    """
    Base registration form.
    """
    class Meta(UserCreationForm.Meta):
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            'password1',
            'password2',
        ]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        email_field = User.get_email_field_name()
        self.fields[email_field].required = True


class AuthenticationForm(BaseAuthenticationForm):
    """
    Base authentication form.
    """
