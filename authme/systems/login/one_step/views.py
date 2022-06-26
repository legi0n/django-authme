from django.contrib.auth import get_user_model, login
from authme._types import Form
from authme.views import LoginView as BaseLoginView

__all__ = [
    'LoginView',
]


User = get_user_model()


class LoginView(BaseLoginView):
    def process(self, form: Form) -> User:
        user = form.get_user()
        login(self.request, user)
        return user
