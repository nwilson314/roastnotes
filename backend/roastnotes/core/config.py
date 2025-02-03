from dotenv import load_dotenv

load_dotenv()

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "dev"

    # Database Configuration
    CONNECTION_STRING: str = ""

    # Local database settings
    DB_USER: str = "roastnotes"
    DB_PASSWORD: str = "roast123"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "roastnotes"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Create settings instance
settings = Settings()
