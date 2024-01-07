from typing import Text
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings class.
    """

    # Twelve Labs
    BASE_API_URL: Text = "https://api.twelvelabs.io"
    API_VERSION: Text = "v1.1"
    DEFAULT_ENGINE: Text = "marengo2.5"
    TASK_STATUS_POLLING_INTERVAL: int = 5


settings = Settings()