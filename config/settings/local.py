from .base import *  # noqa

DEBUG = True

LOGGING = {
    "version": 1,
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
    # "loggers": {
    #     "django.db.backends": {
    #         "handlers": ["console"],
    #         "level": "DEBUG",
    #     },
    # },
}
