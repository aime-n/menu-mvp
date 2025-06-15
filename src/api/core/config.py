from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache # For caching the settings instance

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

    LLM_PROVIDER: str = "openrouter"

    OPENAI_API_KEY: SecretStr = Field(default_factory=lambda: SecretStr("")) # Use SecretStr for keys
    OPENROUTER_API_KEY: SecretStr = Field(default_factory=lambda: SecretStr(""))
    BASE_URL_OPENROUTER: str = "https://openrouter.ai/api/v1"
    TIMEOUT: int = 600

    LLAMA_MODEL: str = "nvidia/llama-3.3-nemotron-super-49b-v1:free"
    GEMMA_3_1B_MODEL: str = "google/gemma-3-1b-it:free"
    GEMMA_3_27B_MODEL: str = "google/gemma-3-27b-it:free"
    DEEPSEEK_V3_MODEL: str = "deepseek/deepseek-chat-v3-0324:free"
    DEEPSEEK_R1_MODEL: str = "deepseek/deepseek-r1-zero:free"

    # TODO: Add Google Gemini Keys?
    
    # TODO Database configuration
    # host, port, name, user, password

@lru_cache()
def get_settings():
    """
    Returns a cached instance of the Settings class.
    This ensures that .env is loaded only once.
    """
    return Settings()

# Instantiate settings once, to be imported elsewhere
settings = get_settings()
