from server.config.settings import Settings


def get_log_config(settings: Settings) -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "()": "uvicorn.logging.DefaultFormatter",
                "format": "%(asctime)s %(levelprefix)-9s %(name)s: %(message)s",
            },
            "json": {
                "()": "server.infrastructure.logging.formatters.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "console" if settings.server_mode == "local" else "json",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "DEBUG" if settings.debug else "INFO",
            },
            "sqlalchemy.engine": {
                "handlers": ["default"] if settings.debug else [],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["default"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
