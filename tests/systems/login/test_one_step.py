from django.contrib.auth import get_user_model, SESSION_KEY
from django.test.utils import override_settings
from tests.cases import TestCase


User = get_user_model()


@override_settings(
    ROOT_URLCONF='authme.shortcuts.one_step.urls'
)
class TestLoginView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(
            username='testuser', password='password', email='testuser@example.com'
        )

    def test_valid_login(self):
        response = self.client.post(
            '/login/',
            {
                'username': 'testuser',
                'password': 'password',
            }
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_invalid_login(self):
        response = self.client.post(
            '/login/',
            {
                'username': 'testuser',
                'password': 'pasword',
            }
        )
        self.assertNotIn(SESSION_KEY, self.client.session)