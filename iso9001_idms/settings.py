import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'please-change-me-to-a-secure-random-string-with-50+chars-CHANGE_THIS'
)
# Default to True for local development; set DJANGO_DEBUG=false in prod environment
DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('1', 'true', 'yes')
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'core',
    'documents',
    'analysis',
    'audits',
]

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.KeycloakOIDCMiddleware',
]

ROOT_URLCONF = 'iso9001_idms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'iso9001_idms.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'iso9001_idms'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Security hardening defaults when running in production
if not DEBUG:
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', 60))
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
else:
    # In development keep these off to avoid interfering with local workflows
    SECURE_HSTS_SECONDS = 0
    SECURE_SSL_REDIRECT = False

# Keycloak OIDC Settings
"""
Keycloak server URL.
Default uses port 8081 to avoid conflicts with local Jenkins on 8080.
If you run Keycloak on another port, override this with the environment variable.
"""
KEYCLOAK_SERVER_URL = os.environ.get('KEYCLOAK_SERVER_URL', 'http://127.0.0.1:8081')
KEYCLOAK_REALM = os.environ.get('KEYCLOAK_REALM', 'iso9001-realm')
KEYCLOAK_CLIENT_ID = os.environ.get('KEYCLOAK_CLIENT_ID', 'iso9001-client')
KEYCLOAK_CLIENT_SECRET = os.environ.get('KEYCLOAK_CLIENT_SECRET', '')
KEYCLOAK_REDIRECT_URI = os.environ.get('KEYCLOAK_REDIRECT_URI', 'http://127.0.0.1:8000/accounts/callback/')
KEYCLOAK_LOGOUT_REDIRECT_URI = os.environ.get('KEYCLOAK_LOGOUT_REDIRECT_URI', 'http://127.0.0.1:8000/')
KEYCLOAK_PUBLIC_KEY = os.environ.get('KEYCLOAK_PUBLIC_KEY', '')

# Fallback to local auth if Keycloak is unavailable
USE_KEYCLOAK = os.environ.get('USE_KEYCLOAK', 'true').lower() == 'true'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/post-login/'
LOGOUT_REDIRECT_URL = '/accounts/logout/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Simple console logging for development so debug messages (e.g. auth_url) appear
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
