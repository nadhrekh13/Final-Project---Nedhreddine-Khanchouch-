import os
from enum import Enum


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class Settings:
    APP_NAME: str = "Task Management API"
    APP_VERSION: str = "1.0.0"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    ENVIRONMENT: Environment = Environment(
        os.getenv("ENVIRONMENT", "development")
    )
    DATA_FILE: str = os.getenv("DATA_FILE", "tasks.jsonl")
    TEST_DATA_FILE: str = os.getenv("TEST_DATA_FILE", "tasks_test.jsonl")

    @property
    def data_file(self) -> str:
        if self.ENVIRONMENT == Environment.TESTING:
            return self.TEST_DATA_FILE
        return self.DATA_FILE


settings = Settings()
