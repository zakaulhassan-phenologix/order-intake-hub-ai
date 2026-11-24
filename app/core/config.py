from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Order Intake AI"
    app_version: str = "0.1.0"
    environment: str = "dev"

    # Amazon Bedrock
    aws_region: str = "us-east-1"
    bedrock_model_id: str = ""

    # Langfuse
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = ""

    # Database
    database_url: str = ""

    # Service-to-service auth
    service_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
