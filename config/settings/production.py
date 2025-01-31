from .base import *  # noqa

DEBUG = False

ALLOWED_HOSTS = env.str("ALLOWED_HOSTS", "127.0.0.1").split(",")  # noqa

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = None
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_CONTENT_TYPE_NOSNIFF = False

CSRF_TRUSTED_ORIGINS = env.str("CSRF_TRUSTED_ORIGINS", "http://localhost:8000").split(",")  # noqa

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "celery": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "celery.task": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "celery.worker": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}

CELERY_WORKER_HIJACK_ROOT_LOGGER = False
CELERY_WORKER_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s] %(message)s"
CELERY_WORKER_TASK_LOG_FORMAT = "[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s"
