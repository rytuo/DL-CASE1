from pydantic import FilePath
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # CORS
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = ["*"]
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    MODEL_PATH: FilePath = "models/best.pt"

    # 50 MB
    MAX_FILE_SIZE: int = 52_428_800


settings = Settings()
