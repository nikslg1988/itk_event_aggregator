import os

from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("POSTGRES_CONNECTION_STRING") or "None"
EVENTS_PROVIDER_BASE_URL = os.getenv("EVENTS_PROVIDER_BASE_URL")
EVENTS_PROVIDER_API_KEY = os.getenv("EVENTS_PROVIDER_API_KEY")
