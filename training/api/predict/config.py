from functools import lru_cache
from pydantic import BaseSettings
import os


class PredictServerSettings(BaseSettings):
    host: str
    port: int


class PredictApplicationSettings(BaseSettings):
    artifacts_dir_path: str


@lru_cache()
def get_predict_server_settings():
    return PredictServerSettings()


@lru_cache()
def get_predict_application_settings():
    artifacts_dir_path = os.environ['ARTIFACTS_DIR_PATH']
    return PredictApplicationSettings(artifacts_dir_path=artifacts_dir_path)