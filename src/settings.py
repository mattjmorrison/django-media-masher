from os import path
DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = path.abspath(path.dirname(__file__))

ADMINS = (
    ('Matthew J. Morrison', 'mattj.morrison@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '.database',
    }
}

USE_I18N = False
USE_L10N = True
MEDIA_ROOT = path.join(PROJECT_DIR, 'media')
STATIC_ROOT = MEDIA_ROOT
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin-media/'
SECRET_KEY = '-2cmgs7l$5grqwd!x&6241^ah&xx34ki48fwn#ef5s_lm(1@0a4w&v'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'src.urls'

TEMPLATE_DIRS = ( )

INSTALLED_APPS = (
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'debug_toolbar',
    'masher',
    'sample_app',
)

SOUTH_TESTS_MIGRATE = False

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,
    'INTERCEPT_REDIRECTS': False,
}

MASHER_COMPRESS = True