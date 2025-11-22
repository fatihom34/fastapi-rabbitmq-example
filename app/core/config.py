from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Rabbit MQ Example"
    ENVIRONMENT: str = "development"

    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672

    # JWT / Auth
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
