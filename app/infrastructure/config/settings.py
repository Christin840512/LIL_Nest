# infrastructure/config/settings.py
from pydantic_settings import BaseSettings


class JwtSettings(BaseSettings):
    JWT_SECRET_KEY: str = "qazwsx"
    JWT_ALGORITHM: str = "HS256"

class NewebpayEndpoints(BaseSettings):
    MPG: str = "https://core.newebpay.com/MPG/mpg_gateway"
    QUERY: str = "https://core.newebpay.com/API/QueryTradeInfo"
    CANCEL: str = "https://core.newebpay.com/API/CreditCard/Cancel"
    CLOSE: str = "https://core.newebpay.com/API/CreditCard/Close"
    EWALLET_REFUND: str = "https://core.newebpay.com/API/EWallet/refund"

class MockNewebpayEndpoints(BaseSettings):
    MPG: str = "https://ccore.newebpay.com/MPG/mpg_gateway"
    QUERY: str = "https://ccore.newebpay.com/API/QueryTradeInfo"
    CANCEL: str = "https://ccore.newebpay.com/API/CreditCard/Cancel"
    CLOSE: str = "https://ccore.newebpay.com/API/CreditCard/Close"
    EWALLET_REFUND: str = "https://ccore.newebpay.com/API/EWallet/refund"

class NewebpaySecrets(BaseSettings):
    MERCHANT_ID: str = "MS357423624"
    HASH_KEY: str = "FkO3p6tnQeZyrWzNQQifOjfk5NBWtw6Z"
    HASH_IV: str = "C7GqYbF9XQ5rHmHP"


class Settings(BaseSettings):
    jwt: JwtSettings = JwtSettings()
    newebpay_endpoints: NewebpayEndpoints = NewebpayEndpoints()
    newebpay_secrets: NewebpaySecrets = NewebpaySecrets()

class TestSettings(BaseSettings):
    jwt: JwtSettings = JwtSettings()
    newebpay_endpoints: MockNewebpayEndpoints = MockNewebpayEndpoints()
    newebpay_secrets: NewebpaySecrets = NewebpaySecrets()

def get_settings() -> BaseSettings:
    return TestSettings()