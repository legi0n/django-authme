from typing import Any, Union, Optional
from django.test import RequestFactory, TestCase
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.generic.base import View
from django.contrib.auth.models import User
from .factories import UserFactory

__all__ = [
    'HttpCodeTestCase',
    'TestCase',
]


class HttpCodeTestCase(TestCase):
    def assertHttpCode(self, response: str, code: int) -> None:
        self.assertEqual(
            response.status_code, code,
            f'Expected an HTTP {code}, but got HTTP {response.status_code}'
        )

    def assertHttpOK(self, response: HttpResponse) -> None:
        self.assertHttpCode(response, 200)

    def assertHttpRedirect(self, response: HttpResponse) -> None:
        self.assertTrue(
            300 <= response.status_code < 400,
            f'Expected an HTTP 3XX, but got HTTP {response.status_code})'
        )

    def assertHttpUnauthorized(self, response: HttpResponse) -> None:
        self.assertHttpCode(response, 401)

    def assertHttpForbidden(self, response: HttpResponse) -> None:
        self.assertHttpCode(response, 403)


class TestCase(HttpCodeTestCase):
    request_factory_class = RequestFactory
    user_factory_class = UserFactory

    def setUp(self):
        self.RequestFactory = self.request_factory_class
        self.UserFactory = self.user_factory_class

    def build_request(
        self,
        path: Optional[str] = '/',
        user: Optional[Union[User, str]] = None,
        user_kwargs: Any = {}
    ) -> HttpRequest:
        if user == 'anonymous':
            user = self.UserFactory.anonymous()
        else:
            user = self.UserFactory(**user_kwargs)
        request = self.RequestFactory().get(path)
        request.user = user
        return request

    def get_view_response(
        self,
        view: View,
        request: HttpRequest = None
    ) -> HttpResponse:
        if request is None:
            request = self.build_request()
        return view.as_view()(request)
