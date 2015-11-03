def pytest_configure():
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DEBUG_PROPAGATE_EXCEPTIONS=True,
            DATABASES={'default': {'ENGINE': 'django.db.backends.sqlite3',
                       'NAME': ':memory:'}},
            INSTALLED_APPS=(
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sites',
                'changuito',
                'tests',
            ),
            SITE_ID=1,
            SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
            MIDDLEWARE_CLASSES=(),
        )

        try:
            import django
            django.setup()
        except AttributeError:
            pass
