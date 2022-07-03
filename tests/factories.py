import factory
import faker
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser, User

__all__ = [
    "UserFactory",
]


f = faker.Faker()


class UserFactory(factory.django.DjangoModelFactory):

    username = f.user_name()
    first_name = f.first_name()
    last_name = f.last_name()
    email = f.email()
    password = make_password(f.password())

    class Meta:
        model = User

    @classmethod
    def anonymous(cls) -> AnonymousUser:
        return AnonymousUser()
