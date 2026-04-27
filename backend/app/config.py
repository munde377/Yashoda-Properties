from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    database_url: str = "sqlite:///./app.db"

    # WhatsApp API integration settings
    whatsapp_api_url: str = ""
    whatsapp_api_key: str = ""

    # Frontend URL for CORS and redirects
    frontend_url: str = "http://localhost:5173"

    # Frontend dist path for static file serving
    frontend_dist_path: str = "/app/frontend/dist"

    # JWT authentication settings
    jwt_secret_key: str = "CHANGE_THIS_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 120

    class Config:
        env_file = ".env"


# Global settings instance
settings = Settings()
