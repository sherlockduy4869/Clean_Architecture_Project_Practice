
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class EnvConfig(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    model_config = ConfigDict(
        env_file = '.env.dev',
        env_file_encoding = 'utf-8',
        case_sensitive = False,
        extra = 'ignore'
    )