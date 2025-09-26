import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 1))
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ADMIN_KEY = os.getenv("ADMIN_KEY")

config = Config()