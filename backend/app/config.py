import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database URLs for different modules
    DATABASE_URL_A: str = os.getenv("DATABASE_URL_A", "postgresql://postgres:postgres@localhost:5432/database1")
    DATABASE_URL_B: str = os.getenv("DATABASE_URL_B", "postgresql://postgres:postgres@localhost:5432/database2")
    
    # Legacy support for backward compatibility
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",  # React dev server
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # App Settings
    APP_NAME: str = "Cursor Easy Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"

settings = Settings() 