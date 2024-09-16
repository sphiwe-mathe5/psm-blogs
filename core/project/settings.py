import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = Path(__file__).resolve().parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='.vercel.app,127.0.0.1,.com').split(',')

ADMIN_PATH = config('ADMIN_PATH')



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    #'whitenoise.runserver_nostatic',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'submit',
    'crispy_forms',
    'emails',
   'django_otp',
   'django_otp.plugins.otp_totp',
    'axes',
    #'crispy_bootstrap4',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'core.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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




WSGI_APPLICATION = 'core.project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}

CRISPY_TEMPLATE_PACK = 'bootstrap4'  # or 'bootstrap3' depending on your Bootstrap version




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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True


AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]


STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "project/static")]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

from google.oauth2 import service_account
GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    os.path.join(BASE_DIR, 'credential.json'))

DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
GS_PROJECT_ID = 'civic-karma-435316-n7'
GS_BUCKET_NAME = 'psmadmin-bucket'
MEDIA_ROOT = "media/"
UPLOAD_ROOT = 'media/uploads'
MEDIA_URL = f'https://storage.googleapis.com/{GS_BUCKET_NAME}/'
    
#MEDIA_URL = '/media/'
#MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('ADMIN_EMAIL')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')
ADMIN_EMAIL = config('ADMIN_EMAIL')


SILENCED_SYSTEM_CHECKS = config('SILENCED_SYSTEM_CHECKS', cast=Csv())

AXES_FAILURE_LIMIT = config('AXES_FAILURE_LIMIT', cast=int)

AXES_COOLOFF_TIME = 1

AXES_ONLY_ADMIN_SITE = config('AXES_ONLY_ADMIN_SITE', cast=bool)

AXES_LOCKOUT_TEMPLATE = config('AXES_LOCKOUT_TEMPLATE')

AXES_LOCKOUT_URL = config('AXES_LOCKOUT_URL')
AXES_USERNAME_FORM_FIELD = config('AXES_USERNAME_FORM_FIELD')

AXES_RESET_ON_SUCCESS = config('AXES_RESET_ON_SUCCESS', cast=bool)

AXES_NEVER_LOCKOUT_WHITELIST = config('AXES_NEVER_LOCKOUT_WHITELIST',
                                      cast=bool)
AXES_IP_WHITELIST = config('AXES_IP_WHITELIST', cast=Csv())

AXES_ENABLE_ACCESS_FAILURE_LOG = config('AXES_ENABLE_ACCESS_FAILURE_LOG',
                                        cast=bool)

AXES_RESET_ON_SUCCESS = config('AXES_RESET_ON_SUCCESS', cast=bool)

AXES_LOCKOUT_PARAMETERS = config('AXES_LOCKOUT_PARAMETERS', cast=Csv())


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
if DEBUG == False:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 15768000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_REFERRER_POLICY = 'same-origin'
    SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
    SESSION_COOKIE_NAME = '__Host-sessionid'
    CSRF_COOKIE_NAME = '__Host-csrftoken'

#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


#RECAPTCHA_PUBLIC_KEY = '6LfbMz0qAAAAAPKxZsJX27CmO3WYDBqAWwjybCG_'
#RECAPTCHA_PRIVATE_KEY = '6LfbMz0qAAAAAKNiMJAoajTL8vbd9tKQyCuS6U4I'
#RECAPTCHA_REQUIRED_SCORE = 0.85

LOGIN_REDIRECT_URL = 'index'
LOGIN_URL = 'login'
