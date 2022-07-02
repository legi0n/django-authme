from django.contrib.auth import get_user_model, SESSION_KEY
from django.test.utils import override_settings
from tests.cases import TestCase


User = get_user_model()


@override_settings(
    ROOT_URLCONF='authme.shortcuts.one_step.urls'
)
class TestLogoutView(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(
            username='testuser', password='password', email='testuser@example.com'
        )
    
    def test_anonymous_logout(self):
        response = self.client.post('/logout/')
        self.assertRedirects(response, '/login/?next=/logout/')

    def test_user_logout(self):
        self.client.force_login(self.u1)
        self.assertIn(SESSION_KEY, self.client.session)

        self.client.post('/logout/')
        self.assertNotIn(SESSION_KEY, self.client.session)
