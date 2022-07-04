from typing import Any, Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from authme._types import FormType, HttpRequestType, HttpResponseType, UserType
from authme.conf.settings import app_settings
from authme.forms import AuthenticationForm, RegistrationForm
from authme.mixins import LoginRequiredMixin, RedirectURLMixin

__all__ = [
    "SignupView",
    "LoginView",
]


UserModel = get_user_model()


class BaseTemplateView(RedirectURLMixin, TemplateView):
    template_name: str = "authme/base.html"
    next_page: Optional[str] = None

    def process(self) -> None:
        """
        Override to process the data before redirecting.
        """
        raise NotImplementedError

    @method_decorator(never_cache)
    def dispatch(
        self, request: HttpRequestType, *args: Any, **kwargs: Any
    ) -> HttpResponseType:
        self.process()
        return super().dispatch(request, *args, **kwargs)


class BaseView(RedirectURLMixin, FormView):
    form_class: FormType = None
    success_url: Optional[str] = None
    template_name: str = "authme/base_form.html"
    redirect_authenticated_user: bool = False

    def get_success_url(self, user: Optional[UserType] = None) -> str:
        return super().get_success_url()

    def form_valid(self, form: FormType) -> HttpResponseType:
        return HttpResponseRedirect(self.get_success_url(self.process(form)))

    def process(self, form: FormType) -> Any:
        """
        Override to process the form after validation.
        """
        raise NotImplementedError

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(
        self, request: HttpRequestType, *args: Any, **kwargs: Any
    ) -> HttpResponseType:
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. "
                    "Check that your redirect_authenticated_user "
                    "doesn't point to an authentication page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


class SignupView(BaseView):
    """
    Base signup view.
    """

    form_class: FormType = RegistrationForm
    template_name: str = "authme/base_signup.html"
    redirect_authenticated_user: bool = app_settings.SIGNUP_REDIRECT_AUTHENTICATED
    next_page: str = app_settings.SIGNUP_REDIRECT_URL
    disallowed_url: Optional[str] = None

    def get_disallowed_url(self) -> str:
        disallowed_url = self.disallowed_url or app_settings.SIGNUP_DISALLOWED_URL
        if not disallowed_url:
            class_name = self.__class__.__name__
            raise ImproperlyConfigured(
                f"{class_name} is missing the disallowed_url attribute."
                f"Define {class_name}.disallowed_url, `SIGNUP_DISALLOWED_URL`"
                "in settings.AUTHME, or override "
                f"{class_name}.get_disallowed_url()."
            )
        return str(disallowed_url)

    def registration_allowed(self) -> bool:
        return app_settings.SIGNUP_ALLOWED

    def dispatch(
        self, request: HttpRequestType, *args: Any, **kwargs: Any
    ) -> HttpResponseType:
        if not self.registration_allowed():
            return HttpResponseRedirect(self.get_disallowed_url())
        return super().dispatch(request, *args, **kwargs)


class LoginView(BaseView):
    """
    Base login view.
    """

    form_class: FormType = AuthenticationForm
    template_name: str = "authme/base_login.html"
    redirect_authenticated_user: bool = app_settings.LOGIN_REDIRECT_AUTHENTICATED
    next_page: str = app_settings.LOGIN_REDIRECT_URL


class LogoutView(LoginRequiredMixin, BaseTemplateView):
    """
    Base logout view.
    """

    template_name: str = "authme/base_logout.html"
    next_page: Optional[str] = app_settings.LOGOUT_REDIRECT_URL

    def post(
        self, request: HttpRequestType, *args: Any, **kwargs: Any
    ) -> HttpResponseType:
        self.process()
        success_url = self.get_success_url()
        if success_url != request.get_full_path():
            return HttpResponseRedirect(success_url)
        return super().get(request, *args, **kwargs)

    @method_decorator(never_cache)
    @method_decorator(csrf_protect)
    def dispatch(
        self, request: HttpRequestType, *args: Any, **kwargs: Any
    ) -> HttpResponseType:
        return super().dispatch(request, *args, **kwargs)
