#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_version: str = "0.0.1"
    app_name: str = "Deep Learning FastAPI Backend"
    api_prefix: str = "/api"
    database_url: str = "sqlite:///./test.db"

    is_debug: bool = False
    default_model_path: str

    secret_key: SecretStr
    algorithm: str = "HS256"

    class Config:
        env_file = "env"
        env_file_encoding = "utf-8"


settings = Settings()
SECRET_KEY = settings.secret_key.get_secret_value()
DEFAULT_MODEL_PATH = settings.default_model_path
ALGORITHM = settings.algorithm
