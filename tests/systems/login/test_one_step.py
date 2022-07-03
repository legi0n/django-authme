from django.contrib.auth import SESSION_KEY, get_user_model
from django.test.utils import override_settings

from tests.cases import TestCase

User = get_user_model()


@override_settings(ROOT_URLCONF="authme.shortcuts.one_step.urls")
class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.u1 = User.objects.create_user(
            username="testuser", password="password", email="testuser@example.com"
        )

    def test_valid_login(self):
        self.client.post(
            "/login/",
            {
                "username": "testuser",
                "password": "password",
            },
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_invalid_login(self):
        self.client.post(
            "/login/",
            {
                "username": "testuser",
                "password": "pasword",
            },
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_redirect_authenticated_user(self):
        self.client.force_login(self.u1)
        self.assertIn(SESSION_KEY, self.client.session)

        response = self.client.get("/login/?next=/logout/")
        self.assertRedirects(response, "/logout/")
