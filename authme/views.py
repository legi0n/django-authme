from typing import Any, Optional
from django.views.generic.edit import FormView
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ImproperlyConfigured
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect
from authme._types import Form
from authme.conf.settings import app_settings
from authme.forms import RegistrationForm, AuthenticationForm

__all__ = [
    'SignupView',
    'LoginView',
]


User = get_user_model()


class BaseView(FormView):
    form_class = None
    success_url = None
    template_name = None

    def get_success_url(self, user: User = None) -> str:
        return super().get_success_url()

    def form_valid(self, form: Form) -> HttpResponse:
        return HttpResponseRedirect(self.get_success_url(self.process(form)))

    def process(self, form: Form) -> Any:
        """
        Override to process the form after validation.
        """
        raise NotImplementedError

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)


class SignupView(BaseView):
    """
    Base signup view.
    """
    form_class: Form = RegistrationForm
    template_name: str = 'authme/base_signup.html'
    disallowed_url: Optional[str] = None

    def get_success_url(self, user: User = None) -> str:
        success_url = (
            self.success_url or app_settings.SIGNUP_REDIRECT_URL
        )
        if not success_url:
            class_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f'{class_name} is missing the success_url attribute. '
                f'Define {class_name}.success_url, '
                '`SIGNUP_REDIRECT_URL` in settings.AUTHME, '
                f'or override {class_name}.get_success_url().'
            )
        return str(success_url)

    def get_disallowed_url(self) -> str:
        disallowed_url = self.disallowed_url or app_settings.SIGNUP_DISALLOWED_URL
        if not disallowed_url:
            class_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f'{class_name} is missing the disallowed_url attribute. Define '
                f'{class_name}.disallowed_url, `SIGNUP_DISALLOWED_URL` in settings.AUTHME, '
                f'or override {class_name}.get_disallowed_url().'
            )
        return str(disallowed_url)

    def registration_allowed(self) -> bool:
        return app_settings.SIGNUP_ALLOWED

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.registration_allowed():
            return HttpResponseRedirect(self.get_disallowed_url())
        return super().dispatch(request, *args, **kwargs)


class LoginView(BaseView):
    """
    Base login view.
    """
    form_class: Form = AuthenticationForm
    template_name: str = 'authme/base_login.html'

    def get_success_url(self, user: User = None) -> str:
        success_url = (
            self.success_url or app_settings.LOGIN_REDIRECT_URL
        )
        if not success_url:
            class_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f'{class_name} is missing the success_url attribute. '
                f'Define {class_name}.success_url, '
                '`LOGIN_REDIRECT_URL` in settings.AUTHME, '
                f'or override {class_name}.get_success_url().'
            )
        return str(success_url)
