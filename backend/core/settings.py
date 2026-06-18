from decouple import config
from pathlib import Path
from urllib.parse import urlparse
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def csv_config(name, default=""):
    return [item.strip() for item in config(name, default=default).split(",") if item.strip()]


def with_https(value):
    if not value:
        return ""
    value = value.strip().rstrip("/")
    if value.startswith(("http://", "https://")):
        return value
    return f"https://{value}"


SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = csv_config(
    "ALLOWED_HOSTS",
    default="localhost,127.0.0.1,.liara.run,api.arminghajari.ir"
)

# =========================
# Apps
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'drf_spectacular',
    'storages',
    'corsheaders',

    'portfolio',
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # ← باید اول باشه
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = "core.wsgi.application"

# =========================
# Templates
# =========================
TEMPLATES = [{
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
}]

# =========================
# Database
# =========================
DATABASE_URL = config('DATABASE_URL', default='')

if DATABASE_URL:
    parsed_db = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed_db.path.lstrip('/') or 'postgres',
            'USER': parsed_db.username or '',
            'PASSWORD': parsed_db.password or '',
            'HOST': parsed_db.hostname or 'localhost',
            'PORT': str(parsed_db.port or 5432),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='portfolio'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default=''),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# =========================
# Static files
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# =========================
# S3 / Liara Object Storage
# =========================
AWS_ACCESS_KEY_ID = config("LIARA_ACCESS_KEY", default="")
AWS_SECRET_ACCESS_KEY = config("LIARA_SECRET_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("LIARA_BUCKET_NAME", default=config("BUCKET_NAME", default=""))
AWS_S3_ENDPOINT_URL = with_https(config("LIARA_ENDPOINT_URL", default=config("LIARA_ENDPOINT", default="")))
LIARA_PUBLIC_MEDIA_URL = with_https(config("LIARA_PUBLIC_MEDIA_URL", default=""))

AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = "public-read"
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

_endpoint_host = AWS_S3_ENDPOINT_URL.replace("https://", "").replace("http://", "") if AWS_S3_ENDPOINT_URL else ""
AWS_S3_CUSTOM_DOMAIN = (
    LIARA_PUBLIC_MEDIA_URL.replace("https://", "").replace("http://", "").rstrip("/")
    if LIARA_PUBLIC_MEDIA_URL
    else f"{_endpoint_host}/{AWS_STORAGE_BUCKET_NAME}"
    if _endpoint_host and AWS_STORAGE_BUCKET_NAME
    else ""
)
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/" if AWS_S3_CUSTOM_DOMAIN else "/media/"

# =========================
# CORS / CSRF
# =========================
CORS_ALLOWED_ORIGINS = csv_config(
    "CORS_ALLOWED_ORIGINS",
    default="""
http://localhost:5173,
http://127.0.0.1:5173,
https://arminghajari.ir,
https://www.arminghajari.ir
"""
)

CSRF_TRUSTED_ORIGINS = csv_config(
    "CSRF_TRUSTED_ORIGINS",
    default="""
https://arminghajari.ir,
https://www.arminghajari.ir,
https://api.arminghajari.ir,
https://*.liara.run,
http://localhost:5173,
http://127.0.0.1:5173
"""
)
CORS_ALLOW_ALL_ORIGINS = False  # هیچ‌وقت True نذار روی production

# =========================
# DRF
# =========================
# =========================
# DRF
# =========================
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Personal Portfolio API',
    'DESCRIPTION': 'API سایت شخصی',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAdminUser'],
}

# =========================
# Security
# =========================
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    USE_X_FORWARDED_HOST = True
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
# =========================
# Storage backends
# =========================
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# =========================
# Upload limits
# =========================
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024