"""
Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# The following import and function are taken verbatim from
#  Two Scoops of Django, pgs. 39-40.

# Normally you should not import ANYTHING from Django directely
#  into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, default=None):
    """ Get the environment variable or return exception. """
    try:
        return os.environ[var_name]
    except KeyError:
        return default
        # error_msg = "Set the %s environment variable" % var_name
        # raise ImproperlyConfigured(error_msg)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(PROJECT_PATH, "apps")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

EXTRA_ALLOWED_HOSTS = get_env_variable("ALLOWED_HOSTS")
if EXTRA_ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(EXTRA_ALLOWED_HOSTS)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Although it's not required that you use the sites framework, it's strongly encouraged
    'django.contrib.sites',
    'django_crontab',
    'bootstrap3',
    'website',
    'data_services',
    'website.apps.om_validate',
    'website.apps.ts_om',
    'website.apps.ts_om_viz',
    'website.apps.ts_om_edit',
    'website.apps.big_brother',
    'website.apps.email',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'website.apps.big_brother.middleware.BigBrotherMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'website.middleware.RedirectionMiddleware',
)

ROOT_URLCONF = 'website.urls'

# Please refer to https://docs.djangoproject.com/en/1.8/ref/contrib/sites/
# for additional information about Django sites framework
SITE_ID = 1

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'website', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.core.context_processors.static',
                "website.context_processors.app_env"
            ],
        },
    },
]

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Your project will probably also have static assets that aren't tied to a particular app. In addition to using
# a static/ directory inside your apps, you can define a list of directories (STATICFILES_DIRS) in your settings
# file where Django will also look for static files.
STATICFILES_DIRS = (
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'apache', 'static')

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(BASE_DIR, 'website', 'media')

SIM_SERVICE_LOCAL_INPUT_DIR = os.path.join(MEDIA_ROOT, "simulations")
SIM_SERVICE_LOCAL_OM_EXECUTABLE = os.path.join(BASE_DIR, 'binaries/om/openMalaria')
if os.name == "nt":
    OM_EXECUTABLE = os.path.join(BASE_DIR, 'binaries', 'om', 'openmalaria.exe')
else:
    OM_EXECUTABLE = os.path.join(BASE_DIR, 'binaries', 'om', 'openMalaria')

LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/?next=/"

# Django logging configuration
# https://docs.djangoproject.com/en/1.8/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'website': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'sim_services_local': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propogate': True,
        }
    },
    "formatters": {
        "simple": {
            "format": "%(levelname)s: [%(name)s:%(lineno)s] %(message)s"
        }
    }
}

OPENMALARIA_EXEC_DIR = os.path.join(BASE_DIR, 'binaries', 'om')

TS_OM_SCENARIOS_DIR = os.path.join(BASE_DIR, 'scenarios')

DATABASE_BACKUP_DIR = MEDIA_ROOT

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CRONTAB_COMMENT used for marking the added contab-lines for removing, default value includes project name
# to distinguish multiple projects on the same host and user
CRONTAB_COMMENT = "base"
