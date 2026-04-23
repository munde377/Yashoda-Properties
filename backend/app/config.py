from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"
    whatsapp_api_url: str = ""
    whatsapp_api_key: str = ""
    frontend_url: str = "http://localhost:5173"
    jwt_secret_key: str = "CHANGE_THIS_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    class Config:
        env_file = ".env"


settings = Settings()
