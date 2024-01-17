from functools import cache

from core.config import MainConfig


@cache
def get_settings() -> MainConfig:
    return MainConfig()
