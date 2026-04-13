from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_HOST: str
    REDIS_PORT: int

    MINIO_ROOT_USER: str | None = None
    MINIO_ROOT_PASSWORD: str | None = None
    MINIO_BUCKET: str | None = None
    S3_ENDPOINT_URL: str | None = None
    AWS_REGION: str | None = None
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()