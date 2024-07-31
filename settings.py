import os

from dotenv import load_dotenv
from pydantic import StrictStr, SecretStr

from pydantic_settings import BaseSettings

load_dotenv()


class ApiSettings(BaseSettings):
    site_api_key: SecretStr = os.getenv("SITE_API_KEY", None)
    site_api_host: StrictStr = os.getenv("SITE_API_HOST", None)
    tg_api_token: SecretStr = os.getenv("TG_API_TOKEN", None)
