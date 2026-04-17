"""
Django settings for core project.
"""

import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    raw_value = os.getenv(name, default)
    return [item.strip() for item in raw_value.split(",") if item.strip()]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-#dh9_2+3_ip4lbz&wpiqa6jo0l9lwz3!u+2$5^4aiui1mfcp#m",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_hostname:
    ALLOWED_HOSTS.append(render_hostname)

CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")
if render_hostname:
    CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "accounts.apps.AccountsConfig",
    "students.apps.StudentsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"


# Database
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}


# Password validation
AUTH_USER_MODEL = "accounts.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# Security settings for reverse proxy platforms such as Render
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG


# CORS
CORS_ALLOW_ALL_ORIGINS = env_bool("CORS_ALLOW_ALL_ORIGINS", default=DEBUG)
if not CORS_ALLOW_ALL_ORIGINS:
    CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", "")


# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}




# # """
# # Django settings for core project.
# # """

# # import os
# # from pathlib import Path
# # import dj_database_url

# # BASE_DIR = Path(__file__).resolve().parent.parent


# # # -----------------------------
# # # ENV HELPERS
# # # -----------------------------
# # def env_bool(name, default=False):
# #     value = os.getenv(name)
# #     if value is None:
# #         return default
# #     return value.strip().lower() in {"1", "true", "yes", "on"}


# # def env_list(name, default=""):
# #     raw_value = os.getenv(name, default)
# #     return [item.strip() for item in raw_value.split(",") if item.strip()]


# # # -----------------------------
# # # SECURITY
# # # -----------------------------
# # SECRET_KEY = os.getenv(
# #     "DJANGO_SECRET_KEY",
# #     "unsafe-secret-key-change-in-production"
# # )

# # DEBUG = env_bool("DJANGO_DEBUG", default=False)  # ✅ IMPORTANT


# # # -----------------------------
# # # ALLOWED HOSTS
# # # -----------------------------
# # ALLOWED_HOSTS = env_list(
# #     "DJANGO_ALLOWED_HOSTS",
# #     default="localhost,127.0.0.1"
# # )

# # render_hostname = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# # if render_hostname:
# #     ALLOWED_HOSTS.append(render_hostname)


# # # -----------------------------
# # # CSRF TRUSTED ORIGINS
# # # -----------------------------
# # CSRF_TRUSTED_ORIGINS = env_list(
# #     "DJANGO_CSRF_TRUSTED_ORIGINS",
# #     default=""
# # )

# # if render_hostname:
# #     CSRF_TRUSTED_ORIGINS.append(f"https://{render_hostname}")


# # # -----------------------------
# # # APPLICATIONS
# # # -----------------------------
# # INSTALLED_APPS = [
# #     "corsheaders",  # ✅ must be first
# #     "django.contrib.admin",
# #     "django.contrib.auth",
# #     "django.contrib.contenttypes",
# #     "django.contrib.sessions",
# #     "django.contrib.messages",
# #     "django.contrib.staticfiles",
# #     "rest_framework",
# #     "accounts.apps.AccountsConfig",
# #     "students.apps.StudentsConfig",
# # ]


# # # -----------------------------
# # # MIDDLEWARE (ORDER FIXED ⚠️)
# # # -----------------------------
# # MIDDLEWARE = [
# #     "django.middleware.security.SecurityMiddleware",
# #     "whitenoise.middleware.WhiteNoiseMiddleware",

# #     "corsheaders.middleware.CorsMiddleware",  # ✅ moved up

# #     "django.contrib.sessions.middleware.SessionMiddleware",
# #     "django.middleware.common.CommonMiddleware",
# #     "django.middleware.csrf.CsrfViewMiddleware",
# #     "django.contrib.auth.middleware.AuthenticationMiddleware",
# #     "django.contrib.messages.middleware.MessageMiddleware",
# #     "django.middleware.clickjacking.XFrameOptionsMiddleware",
# # ]


# # # -----------------------------
# # # URLS / TEMPLATES
# # # -----------------------------
# # ROOT_URLCONF = "core.urls"

# # TEMPLATES = [
# #     {
# #         "BACKEND": "django.template.backends.django.DjangoTemplates",
# #         "DIRS": [],  # you can add BASE_DIR / "templates" if needed
# #         "APP_DIRS": True,
# #         "OPTIONS": {
# #             "context_processors": [
# #                 "django.template.context_processors.request",
# #                 "django.contrib.auth.context_processors.auth",
# #                 "django.contrib.messages.context_processors.messages",
# #             ],
# #         },
# #     },
# # ]

# # WSGI_APPLICATION = "core.wsgi.application"


# # -----------------------------
# # DATABASE
# # -----------------------------
# DATABASES = {
#     "default": dj_database_url.config(
#         default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
#         conn_max_age=600,
#         ssl_require=not DEBUG,
#     )
# }


# # -----------------------------
# # AUTH
# # -----------------------------
# AUTH_USER_MODEL = "accounts.User"

# AUTH_PASSWORD_VALIDATORS = [
#     {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
#     {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
#     {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
#     {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
# ]


# # -----------------------------
# # INTERNATIONALIZATION
# # -----------------------------
# LANGUAGE_CODE = "en-us"
# TIME_ZONE = "UTC"
# USE_I18N = True
# USE_TZ = True


# # -----------------------------
# # STATIC FILES (IMPORTANT ⚠️)
# # -----------------------------
# STATIC_URL = "/static/"
# STATIC_ROOT = BASE_DIR / "staticfiles"

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# # -----------------------------
# # SECURITY FOR RENDER
# # -----------------------------
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SESSION_COOKIE_SECURE = not DEBUG
# CSRF_COOKIE_SECURE = not DEBUG


# # -----------------------------
# # CORS
# # -----------------------------
# CORS_ALLOW_ALL_ORIGINS = env_bool(
#     "CORS_ALLOW_ALL_ORIGINS",
#     default=DEBUG
# )

# if not CORS_ALLOW_ALL_ORIGINS:
#     CORS_ALLOWED_ORIGINS = env_list("CORS_ALLOWED_ORIGINS", "")


# # -----------------------------
# # REST FRAMEWORK
# # -----------------------------
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": [
#         "rest_framework.authentication.SessionAuthentication",
#         "rest_framework.authentication.BasicAuthentication",
#     ],
#     "DEFAULT_PERMISSION_CLASSES": [
#         "rest_framework.permissions.AllowAny",
#     ],
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 10,
# }
