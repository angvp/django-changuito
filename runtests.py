#!/usr/bin/env python
import sys

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "changuito",
        ),
        USE_TZ=True,
        SITE_ID=1,
        MIDDLEWARE_CLASSES=(),
        SECRET_KEY="this-is-a-key-for-testing",
    )


from django.test.utils import get_runner


# Django 1.7 fix for tests
try:
    from django import setup
    setup()
except ImportError:
    pass


def runtests():
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(["changuito", ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
