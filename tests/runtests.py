import argparse
import sys
from pathlib import Path

from django.utils.crypto import get_random_string

BASE_DIR = Path(__file__).resolve()

SETTINGS = {
    "BASE_DIR": BASE_DIR,
    "SECRET_KEY": get_random_string(50),
    "INSTALLED_APPS": [
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "authme",
    ],
    "MIDDLEWARE": [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ],
    "ROOT_URLCONF": "urls",
    "TEMPLATES": [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                ],
            },
        }
    ],
    "DATABASES": {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
}


def run_tests(verbosity: int, interactive: bool):
    from django.conf import settings

    settings.configure(**SETTINGS)

    import django

    django.setup()

    from django.test.utils import get_runner

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=interactive)
    failures = test_runner.run_tests(['.'])
    sys.exit(bool(failures))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Django test suite.")
    parser.add_argument(
        "-v",
        "--verbosity",
        default=1,
        type=int,
        choices=[0, 1, 2, 3],
        help="Verbosity level; 0=minimal output, 1=normal output, 2=all output",
    )
    parser.add_argument(
        "--noinput",
        action="store_false",
        dest="interactive",
        help="Tells Django to NOT prompt the user for input of any kind.",
    )

    options = parser.parse_args()
    run_tests(**vars(options))
