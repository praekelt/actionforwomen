from mama.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mama.sqlite',
    }
}

SENDER = "sender@mail.com"
RECIPIENT = ["admin@mail.com", "admin2@mail.com"]

HOTSOCKET_RESOURCES = {
        "login": "test/login",
        "recharge": "test/recharge",
        "status": "test/status",
        "statement": "test/statement",
        "balance": "test/balance",
    }

HOTSOCKET_USERNAME = "trial_acc_1212"
HOTSOCKET_PASSWORD = "tr14l_l1k3m00n"

# South configuration variables
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SKIP_SOUTH_TESTS = True     # Do not run the south tests as part of our
                            # test suite.
SOUTH_TESTS_MIGRATE = False  # Do not run the migrations for our tests.
                             # We are assuming that our models.py are correct
                             # for the tests and as such nothing needs to be
                             # migrated.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    # DEBUGGING STUFF
INTERNAL_IPS = ("http://127.0.0.1")

# EMAIL
# In order to debug do python smtp hosting on port 1025
EMAIL_HOST = "127.0.0.1"
# EMAIL_HOST_USER = "user"
# EMAIL_HOST_PASSWORD = ""
EMAIL_PORT = 1025
EMAIL_USER_TLS = True
