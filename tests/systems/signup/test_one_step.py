import faker
from django.contrib.auth import get_user_model
from django.test.utils import override_settings
from authme.shortcuts.one_step import SignupView
from tests.cases import TestCase


f = faker.Faker()
User = get_user_model()
valid_user_data = {
    User.USERNAME_FIELD: f.user_name(),
    'email': f.email(),
    'password1': 'MyVeryStrongPassword1',
    'password2': 'MyVeryStrongPassword1',
}


@override_settings(
    ROOT_URLCONF='authme.shortcuts.one_step.urls'
)
class TestSignupView(TestCase):
    @override_settings(AUTHME={'SIGNUP_ALLOWED': False})
    def test_signup_disallowed(self):
        request = self.build_request(user='anonymous')
        self.assertHttpRedirect(self.get_view_response(SignupView, request))
    
    def test_user_saved(self):
        data = valid_user_data.copy()
        self.client.post('/signup/', data)
        user = User.objects.get(username=data['username'])
        self.assertTrue(user in User.objects.all())

    def test_check_user_password(self):
        data = valid_user_data.copy()
        self.client.post('/signup/', data)
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password1']))
