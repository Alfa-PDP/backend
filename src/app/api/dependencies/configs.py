from functools import lru_cache

from app.core.config import MainConfig


@lru_cache
def get_main_config() -> MainConfig:
    return MainConfig()
