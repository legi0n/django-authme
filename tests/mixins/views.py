from authme.mixins import *
from tests.views import TestView

__all__ = [
    'LoginRequiredView',
    'AnonymousRequiredView',
    'StaffUserRequiredView',
    'SuperUserRequiredView',
    'UserPassesTestView',
]


class LoginRequiredView(LoginRequiredMixin, TestView):
    ...


class AnonymousRequiredView(AnonymousRequiredMixin, TestView):
    authenticated_redirect_url = '/authenticated'


class StaffUserRequiredView(StaffUserRequiredMixin, TestView):
    ...


class SuperUserRequiredView(SuperUserRequiredMixin, TestView):
    ...


class UserPassesTestView(UserPassesTestMixin, TestView):
    def test_func(self, user):
        return user.email.split('@')[1] == 'mydomain.com'
