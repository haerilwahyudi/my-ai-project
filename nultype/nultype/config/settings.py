from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:pass@localhost:5432/db"
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
