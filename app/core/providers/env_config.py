from app.core.config.env_config import EnvConfig
from functools import lru_cache

@lru_cache()
def get_env_config() -> EnvConfig:
    return EnvConfig()