from logging import config as logging_config

from app.core.config import MainConfig

VERBOSE_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAUL_LOG_FORMAT = "%(levelprefix)s %(message)s"
ACCESS_LOG_FORMAT = "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s"
LOG_DEFAULT_HANDLERS = ["console"]


def setup_logging(config: MainConfig) -> None:
    logging_dict_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": VERBOSE_LOG_FORMAT,
            },
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": DEFAUL_LOG_FORMAT,
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": ACCESS_LOG_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "level": config.project.log_level,
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": LOG_DEFAULT_HANDLERS,
                "level": config.project.log_level,
            },
            "gunicorn.error": {
                "level": config.project.log_level,
            },
            "gunicorn.access": {
                "handlers": ["access"],
                "level": config.project.log_level,
                "propagate": False,
            },
        },
        "root": {
            "level": config.project.log_level,
            "formatter": "verbose",
            "handlers": LOG_DEFAULT_HANDLERS,
        },
    }

    logging_config.dictConfig(logging_dict_config)
