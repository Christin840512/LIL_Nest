# infrastructure/config/settings.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class BasicSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="ignore",
    )

class JwtSettings(BasicSettings):
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

class NewebpayEndpoints(BasicSettings):
    MPG: str 
    QUERY: str
    CANCEL: str
    CLOSE: str
    EWALLET_REFUND: str

class NewebpaySecrets(BasicSettings):
    MERCHANT_ID: str
    HASH_KEY: str
    HASH_IV: str

class Settings(BasicSettings):
    DATABASE_URL: str
    jwt: JwtSettings = JwtSettings()
    newebpay_endpoints: NewebpayEndpoints = NewebpayEndpoints()
    newebpay_secrets: NewebpaySecrets = NewebpaySecrets()

def get_settings() -> BasicSettings:
    return Settings()