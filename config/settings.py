from pathlib import Path
from decouple import config
from django.templatetags.static import static
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool)
PRODUCTION = config("PRODUCTION", cast=bool)

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # extra
    "drf_yasg",
    "django_filters",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    # local
    "users",
    "tests",
]

MIDDLEWARE = [
    "users.middleware.PrintClientIPMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


if PRODUCTION:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


AUTH_PASSWORD_VALIDATORS = []


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "users.User"

# static files
STATIC_URL = "static/"
STATIC_ROOT = "static"

# media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

PAYME_KEY = config("PAYME_KEY")

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"]
}

UNFOLD = {
    "SITE_TITLE": "Admin Panel",
    "SITE_HEADER": "Iqtidor Academy",
    "SITE_SUBHEADER": "Admin Panel",
    "SITE_ICON": {
        "light": lambda request: "https://i.imgur.com/Bz2ohb1.png",
        "dark": lambda request: "https://i.imgur.com/Bz2ohb1.png"
    },
    "SHOW_HISTORY": True,
    "SITE_DROPDOWN": [
        {
            "icon": "payment",
            "title": "PayMe",
            "link": "https://merchant.payme.uz"
        },
    ],

    "LOGIN": {
        "title": "Kirish",
        "image": lambda request: "https://i.imgur.com/Bz2ohb1.png",
    },

    # "SIDEBAR": {
    #     "show_search": True,
    #     "show_all_applications": False,
    #     "navigation": [
    #         {
    #             "title": "Boshqaruv",
    #             "items": [
    #                 {
    #                     "title": "Foydalanuvchilar",
    #                     "icon": "manage_accounts",
    #                     "link": reverse_lazy("admin:users_user_changelist"),
    #                 },
    #                 {
    #                     "title": "Guruhlar",
    #                     "icon": "group",
    #                     "link": reverse_lazy("admin:users_group_changelist"),
    #                 },
    #                 {
    #                     "title": "To'lovlar",
    #                     "icon": "receipt",
    #                     "link": reverse_lazy("admin:users_transaction_changelist")
    #                 },
    #                 {
    #                     "title": "RASH",
    #                     "icon": "functions",
    #                     "link": reverse_lazy("admin:tests_rash_changelist")
    #                 },
    #                 {
    #                     "title": "Fanlar",
    #                     "icon": "calculate",
    #                     "link": reverse_lazy("admin:tests_subject_changelist")
    #                 },
    #                 {
    #                     "title": "E'lonlar",
    #                     "icon": "campaign",
    #                     "link": reverse_lazy("admin:tests_banner_changelist")
    #                 }
    #             ]
    #         },
    #         {
    #             "title": "DTM",
    #             "separator": True,
    #             "collapsable": True,
    #             "items": [
    #                 {
    #                     "title": "DTMlar",
    #                     "icon": "checklist",
    #                     "link": reverse_lazy("admin:tests_dtm_changelist"),
    #                 },
    #                 {
    #                     "title": "Bloklar",
    #                     "icon": "grid_view",
    #                     "link": reverse_lazy("admin:tests_block_changelist"),
    #                 },
    #                 {
    #                     "title": "Savollar",
    #                     "icon": "grid_view",
    #                     "link": reverse_lazy("admin:tests_test_changelist"),
    #                 },
    #                 {
    #                     "title": "Natijalari",
    #                     "icon": "list",
    #                     "link": reverse_lazy("admin:tests_dtmresult_changelist"),
    #                 }
    #             ]
    #         },
    #         {
    #             "title": "CEFR",
    #             "separator": True,
    #             "collapsable": True,
    #             "items": [
    #                 {
    #                     "title": "CEFRlar",
    #                     "icon": "check_box",
    #                     "link": reverse_lazy("admin:tests_cefr_changelist"),
    #                 },
    #                 {
    #                     "title": "Savollar",
    #                     "icon": "grid_view",
    #                     "link": reverse_lazy("admin:tests_question_changelist"),
    #                 },
    #                 {
    #                     "title": "Natijalari",
    #                     "icon": "list",
    #                     "link": reverse_lazy("admin:tests_cefrresult_changelist"),
    #                 },
    #             ]
    #         },
    #         {
    #             "title": "Xavfsizlik",
    #             "separator": True,
    #             "collapsable": True,
    #             "items": [
    #                 {
    #                     "title": "Ruxsatlar",
    #                     "icon": "security",
    #                     "link": reverse_lazy("admin:auth_group_changelist"),
    #                 },
    #                 {
    #                     "title": "Tokenlar",
    #                     "icon": "security",
    #                     "link": reverse_lazy("admin:authtoken_token_changelist"),
    #                 }
    #             ]
    #         }
    #     ]
    # }

}
