from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"   # bỏ qua các biến môi trường không khai báo
    )

    DATABASE_URL: str = "postgresql+asyncpg://admin:admin@db:5432/cryptolens"
    PROJECT_NAME: str = "CryptoLens AI"
    GEMINI_API_KEY: str = "YOUR_API_KEY_HERE"
    SECRET_KEY: str = "SUPER_SECRET_KEY"

settings = Settings()