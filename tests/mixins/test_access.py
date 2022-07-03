from django.core.exceptions import PermissionDenied

from tests.cases import TestCase

from .views import *


class TestLoginRequiredMixin(TestCase):
    def test_anonymous_user(self):
        request = self.build_request(user="anonymous")
        self.assertHttpRedirect(self.get_view_response(LoginRequiredView, request))

    def test_authenticated_user(self):
        self.assertHttpOK(self.get_view_response(LoginRequiredView))


class TestAnonymousRequiredMixin(TestCase):
    def test_anonymous_user(self):
        request = self.build_request(user="anonymous")
        self.assertHttpOK(self.get_view_response(AnonymousRequiredView, request))

    def test_authenticated_user(self):
        self.assertHttpRedirect(self.get_view_response(AnonymousRequiredView))


class TestStaffUserRequiredMixin(TestCase):
    def test_anonymous_user(self):
        request = self.build_request(user="anonymous")
        self.assertHttpRedirect(self.get_view_response(StaffUserRequiredView, request))

    def test_authenticated_user(self):
        with self.assertRaises(PermissionDenied):
            self.get_view_response(StaffUserRequiredView)

    def test_staff_user(self):
        request = self.build_request(user_kwargs={"is_staff": True})
        self.assertHttpOK(self.get_view_response(StaffUserRequiredView, request))

    def test_super_user(self):
        request = self.build_request(user_kwargs={"is_superuser": True})
        self.assertHttpOK(self.get_view_response(StaffUserRequiredView, request))


class TestSuperUserRequiredMixin(TestCase):
    def test_anonymous_user(self):
        request = self.build_request(user="anonymous")
        self.assertHttpRedirect(self.get_view_response(SuperUserRequiredView, request))

    def test_authenticated_user(self):
        with self.assertRaises(PermissionDenied):
            self.get_view_response(SuperUserRequiredView)

    def test_staff_user(self):
        request = self.build_request(user_kwargs={"is_staff": True})
        with self.assertRaises(PermissionDenied):
            self.get_view_response(SuperUserRequiredView, request)

    def test_super_user(self):
        request = self.build_request(user_kwargs={"is_superuser": True})
        self.assertHttpOK(self.get_view_response(SuperUserRequiredView, request))


class TestUserPassesTestMixin(TestCase):
    def test_user_pass(self):
        request = self.build_request(user_kwargs={"email": "user@mydomain.com"})
        self.assertHttpOK(self.get_view_response(UserPassesTestView, request))

    def test_user_not_pass(self):
        request = self.build_request(user_kwargs={"email": "user@notmydomain.com"})
        with self.assertRaises(PermissionDenied):
            self.get_view_response(UserPassesTestView, request)
