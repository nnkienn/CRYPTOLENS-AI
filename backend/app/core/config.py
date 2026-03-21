from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_HOST: str = "rabbitmq"

    @property
    def DATABASE_URL(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def RABBITMQ_URL(self) -> str:
        return (
            "amqp://"
            f"{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}"
            f"@{self.RABBITMQ_HOST}/"
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
