# -*- coding: utf-8 -*-
#
# This file is part of the VecNet OpenMalaria Portal.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/om
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

# pragma: no cover

from .base import *


ADMINS = [
    ('Alex', 'avyushko@nd.edu'),
]

ALLOWED_HOSTS = [
    '*',
]

SECRET_KEY = get_env_variable("SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': get_env_variable("DATABASE_NAME"),
        'USER': get_env_variable("DATABASE_USER"),
        'PASSWORD': get_env_variable("DATABASE_PASSWORD"),
        'HOST': "127.0.0.1",
        'PORT': "5432",
    }
}

# SMTP server configuration
EMAIL_HOST = "smtp.nd.edu"
EMAIL_PORT = 25
EMAIL_USE_TLS = True
# SMTP Backend: the backend to use for sending emails.
# Overriding development settings (Console backend)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
# Used by mail_managers function
SERVER_EMAIL = "VecNet OpenMalaria Portal <avyushko@nd.edu>"

PYTHON_EXECUTABLE = "/usr/bin/python2.7"
OM_EXECUTABLE = "/opt/portal/aws.vecnet.org/binaries/om/openMalaria"
SIM_SERVICE_LOCAL_OM_EXECUTABLE = "/opt/portal/aws.vecnet.org/binaries/om/openMalaria"
TS_OM_SCENARIOS_DIR = os.path.join(BASE_DIR, 'scenarios')
OPENMALARIA_EXEC_DIR = os.path.join(BASE_DIR, 'binaries', 'om')
SIM_SERVICE_LOCAL_OM_EXECUTABLE = "/opt/portal/aws.vecnet.org/binaries/om/openMalaria"

LOGIN_URL = "/auth/login/"
LOGOUT_URL = "/auth/logout/?next=/"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'formatter': 'withtimestamp'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'WARNING',
            'propagate': True,
        },
        'website': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propogate': True,
        },
        'sim_services_local': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propogate': True,
        }
    },
    "formatters": {
        "simple": {
           "format": "%(levelname)s: [%(name)s:%(lineno)s] %(message)s"
        },
        "withtimestamp": {
           "format": "%(levelname)s:[%(asctime)s] [%(name)s:%(lineno)s] %(message)s"
        }
    }
}


# Supress W004 "You have not set a value for the SECURE_HSTS_SECONDS setting." warning
# Reason: Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
# Supress W019 "You have 'django.middleware.clickjacking.XFrameOptionsMiddleware' in your MIDDLEWARE_CLASSES,
# but X_FRAME_OPTIONS is not set to 'DENY'"
# Reason: Using frames to display html of Qualtrics responses
SILENCED_SYSTEM_CHECKS = ['security.W004', 'security.W019']

# Security options
# https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-CSRF_COOKIE_AGE
CSRF_COOKIE_SECURE = False  # Allow HTTP (without HTTPS)
CSRF_COOKIE_HTTPONLY = False  # Don't set to True just yet - ajaxSetup in common.js depends on that cookie
CSRF_COOKIE_AGE = 60480  # One week
SESSION_COOKIE_SECURE = False # Allow HTTP (without HTTPS)
SESSION_COOKIE_HTTPONLY = True

# Frames as used on this website, so setting to the 'SAMEORIGIN'
X_FRAME_OPTIONS = "SAMEORIGIN"

# Unless your site should be available over both SSL and non-SSL connections, you may want to either
# set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
SECURE_SSL_REDIRECT = False # Allow HTTP (without HTTPS)

# Set the Anti-MIME-Sniffing header X-Content-Type-Options to 'nosniff'.
# This prevents older versions of Internet Explorer and Chrome from performing MIME-sniffing on the response body,
# potentially causing the response body to be interpreted and displayed as a content type other than the declared
# content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set),
# rather than performing MIME-sniffing.
SECURE_CONTENT_TYPE_NOSNIFF = True

# Pages will be served with an 'x-xss-protection: 1; mode=block' header to to activate the browser's
# XSS filtering and help prevent XSS attacks
SECURE_BROWSER_XSS_FILTER = True


try:
    # Optional settings specific to the local system (for example, custom
    # settings on a developer's system).  The file "settings_local.py" is
    # excluded from version control.
    from .settings_local import *
except ImportError:
    pass