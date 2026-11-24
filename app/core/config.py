from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Order Intake AI"
    app_version: str = "0.1.0"
    environment: str = "dev"
    aws_region: str = "us-east-1"
    bedrock_model_id: str = ""
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = ""
    database_url: str = ""
    service_api_key: str = ""
    tesseract_cmd: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
