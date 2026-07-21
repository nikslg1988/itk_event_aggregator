import os

from dotenv import load_dotenv

load_dotenv()

DB_STRING = os.getenv("POSTGRES_CONNECTION_STRING") or "None"
