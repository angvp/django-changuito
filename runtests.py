import sys

from django.conf import settings

settings.configure(
    DEBUG=True,
    USE_TZ=True,
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
        }
    },
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sites",
        "changuito",
    ],
    SITE_ID=1,
)

from django_nose import NoseTestSuiteRunner
from django.test.utils import get_runner


def runtests():
    test_runner = NoseTestSuiteRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(["changuito"])
    sys.exit(failures)

if __name__ == '__main__':
    runtests()
