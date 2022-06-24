from django.test import TestCase
from django.test.utils import override_settings
from authme.conf.settings import app_settings


class TestAuthmeSettings(TestCase):
    def test_default_value(self):
        self.assertEqual(app_settings.SIGNUP_ALLOWED, True)

    @override_settings(AUTHME={'SIGNUP_ALLOWED': False})
    def test_custom_value(self):
        self.assertEqual(app_settings.SIGNUP_ALLOWED, False)

    def test_invalid_setting(self):
        with self.assertRaises(AttributeError):
            app_settings.INVALID_SETTING
