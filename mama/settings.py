# Django settings for project project.

import os

from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

PATH = os.getcwd()

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Shaun Sephton', 'connect@shaunsephton.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'mama',                      # Or path to database file if using sqlite3.
        'USER': 'mama',                      # Not used with sqlite3.
        'PASSWORD': 'Twhq627Yt',                  # Not used with sqlite3.
        'HOST': '10.53.47.226',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Africa/Johannesburg'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PATH, 'static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'tk1t&n3^r1)yk%ss3wxd79nw*z&__@bnt*7!2pbv7#9_)lepax'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "preferences.context_processors.preferences_cp",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'likes.middleware.SecretBallotUserIpUseragentMiddleware',
)

ROOT_URLCONF = 'mama.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(os.path.dirname(__file__), "templates"),
)

INSTALLED_APPS = (
    'object_tools',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'post',
    'mama',
    'category',
    'ckeditor',
    'export',
    'generate',
    'google_credentials',
    'haystack',
    'jmbo',
    'likes',
    'moderator',
    'photologue',
    'poll',
    'publisher',
    'preferences',
    'secretballot',
    'sites_groups',
    'south',
    'south_admin',
    'userprofile',
    'gunicorn',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CKEDITOR_UPLOAD_PATH = os.path.join(PATH, 'media/uploads')

# Since we monkey-patch color field to category, override
# categories migration scripts with our own.
# Also preferences __module__ override requires our own migrations.
SOUTH_MIGRATION_MODULES = {
    'category': 'mama.migrations_category',
    'preferences': 'mama.migrations_preferences',
}

USER_PROFILE_MODULE = 'mama.UserProfile'

# If no 'next' value found during login redirect home.
LOGIN_REDIRECT_URL = '/'

HAYSTACK_SITECONF = 'mama.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PATH, 'whoosh.index')

EMAIL_SUBJECT_PREFIX = '[MAMA] '

AMBIENT_API_KEY = 'A363FDC5-32F6-4891-8722-04BA2D6AEBA3'
AMBIENT_GATEWAY_PASSWORD = 'm4m45m5'

MODERATOR = {
    'CLASSIFIER': 'moderator.storage.RedisClassifier',
    'CLASSIFIER_CONFIG': {
        'host': 'localhost',
        'port': 6379,
        'db': 8,
        'password': None,
        'socket_timeout': None,
        'connection_pool': None,
        'charset': 'utf-8',
        'errors': 'strict',
        'unix_socket_path': None,
    },
    'HAM_CUTOFF': 0.3,
    'SPAM_CUTOFF': 0.7,
    'ABUSE_CUTOFF': 3,
}

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# Set session cookie age to 1 year, meaning sessions are valid for up to 1 year.
SESSION_COOKIE_AGE = 31536000

GA_CLIENT_ID = '862858405572.apps.googleusercontent.com'
GA_CLIENT_SECRET = 'VXUxb2A6xUyYADGSKjb2h9Op'
GA_SCOPE = 'https://www.googleapis.com/auth/analytics.readonly'
GA_REDIRECT_URI = 'http://askmama.mobi/google-credentials/callback'

SERIALIZATION_MODULES = {
    'csv': 'snippetscream.csv_serializer',
}

client = Client('http://a63d3e29a4e9453c9883663cb3159469:471fe88edf274035bb8c1285a4db8d21@sentry.praekelt.com/22')
setup_logging(SentryHandler(client))
