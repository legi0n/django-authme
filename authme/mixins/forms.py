from typing import Any, Optional

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import resolve_url
from django.template.loader import render_to_string
from django.utils.http import url_has_allowed_host_and_scheme

from authme._types import HttpRequestType, UserType
from authme.conf.settings import app_settings

__all__ = [
    "RedirectURLMixin",
    "EmailMixin",
]


class RedirectURLMixin:
    next_page: Optional[str] = None
    redirect_field_name: str = REDIRECT_FIELD_NAME
    success_url_allowed_hosts: set = set()

    def get_success_url(self) -> str:
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_redirect_url(self) -> str:
        """
        Return the user-originating redirect URL if it's safe.
        """
        redirect_to = self.request.POST.get(  # type: ignore
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name)  # type: ignore
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),  # type: ignore
        )
        return redirect_to if url_is_safe else ""

    def get_success_url_allowed_hosts(self) -> set:
        return {self.request.get_host(), *self.success_url_allowed_hosts}  # type: ignore

    def get_default_redirect_url(self) -> str:
        """
        Return the default redirect URL.
        """
        if self.next_page:
            return resolve_url(self.next_page)
        raise ImproperlyConfigured("No URL to redirect to. Provide a next_page.")


class EmailMixin:
    email_subject_template: Optional[str] = None
    email_body_template: Optional[str] = None

    def get_email_context(self, **kwargs: Any) -> dict:
        """
        Override this method to change the email context.
        """
        return kwargs

    def send_email(
        self,
        user: Optional[UserType] = None,
        request: Optional[HttpRequestType] = None,
    ) -> None:
        if not user:
            if not request:
                raise ValueError(
                    "A user or request must be specified to send an email."
                )
            else:
                user = request.user

        context = self.get_email_context()
        subject = "".join(
            render_to_string(
                template_name=self.email_body_template, context=context, request=request
            ).splitlines()
        )
        message = render_to_string(
            template_name=self.email_body_template, context=context, request=request
        )
        user.send_email(subject, message, app_settings.DEFAULT_FROM_EMAIL)
