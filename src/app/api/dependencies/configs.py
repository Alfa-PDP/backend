from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.core.config import MainConfig


@lru_cache
def get_main_config() -> MainConfig:
    return MainConfig()


MainConfigDep = Annotated[MainConfig, Depends(get_main_config)]
