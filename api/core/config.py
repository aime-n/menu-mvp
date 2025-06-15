from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache # For caching the settings instance
from api.schemas.llm import ModelProvider, ModelName


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding = "utf-8",
        case_sensitive=True,
        extra='ignore')

    PROJECT_NAME: str = "Menu AI API"
    PROJECT_VERSION: str = "0.1.0"

    LLM_PROVIDER: ModelProvider = ModelProvider.OPENROUTER

    OPENAI_API_KEY: SecretStr = Field(default_factory=lambda: SecretStr("")) # Use SecretStr for keys
    OPENROUTER_API_KEY: SecretStr = Field(default_factory=lambda: SecretStr(""))
    BASE_URL_OPENROUTER: str = "https://openrouter.ai/api/v1"
    TIMEOUT: int = 600

    DEFAULT_MODEL: ModelName = ModelName.DEEPSEEK_V3_MODEL

    # TODO: Add Google Gemini Keys?
    
    SUPABASE_URL: SecretStr = Field(default_factory=lambda: SecretStr(""))
    SUPABASE_KEY: SecretStr = Field(default_factory=lambda: SecretStr(""))
    SUPABASE_DB_PASSWORD: SecretStr = Field(default_factory=lambda: SecretStr(""))
    SUPABASE_HOST: str = Field(default_factory=lambda: SecretStr(""))  
    DATABASE_URL: str = Field(default_factory=lambda: SecretStr(""))


@lru_cache()
def get_settings():
    """
    Returns a cached instance of the Settings class.
    This ensures that .env is loaded only once.
    """
    return Settings()

# Instantiate settings once, to be imported elsewhere
settings = get_settings()
