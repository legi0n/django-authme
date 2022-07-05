import faker
from django.contrib.auth import get_user_model

from authme.forms import AuthenticationForm, RegistrationForm
from tests.cases import TestCase

f = faker.Faker()
User = get_user_model()
valid_user_data = {
    User.USERNAME_FIELD: f.user_name(),
    "email": f.email(),
    "password1": "MyVeryStrongPassword1",
    "password2": "MyVeryStrongPassword1",
}


class TestRegistrationForm(TestCase):
    def test_password_fields(self):
        form = RegistrationForm()
        self.assertTrue("password1" in form.fields)
        self.assertTrue("password2" in form.fields)

    def test_email_required(self):
        form = RegistrationForm()
        self.assertTrue(form.fields["email"].required)

    def test_email_validation(self):
        for email in [f.email() for _ in range(5)]:
            data = valid_user_data.copy()
            data["email"] = email
            form = RegistrationForm(data=data)
            self.assertTrue(form.is_valid())

    def test_invalid_email_validation(self):
        for email in [
            "plainaddress",
            "#@%^%#$@#$@#.com",
            "@example.com",
            "email.example.com",
            "email@example@example.com",
        ]:
            data = valid_user_data.copy()
            data["email"] = email
            form = RegistrationForm(data=data)
            self.assertFalse(form.is_valid())
