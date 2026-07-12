from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("APP_NAME")
APP_PORT = int(os.getenv("APP_PORT", 8001))

DATABASE_URL = os.getenv("DATABASE_URL")