import os

from dotenv import load_dotenv

load_dotenv()


def require_env(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"Environment variable '{name}' is not set")
    assert value is not None
    return value


DB_STRING = require_env("POSTGRES_CONNECTION_STRING")
EVENTS_PROVIDER_BASE_URL = require_env("EVENTS_PROVIDER_BASE_URL")
EVENTS_PROVIDER_API_KEY = require_env("EVENTS_PROVIDER_API_KEY")
