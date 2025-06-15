from langchain_openai import ChatOpenAI
from src.api.core.llm_clients import ChatOpenRouter
from src.api.core.config import settings


def get_llm(model_name: str = settings.DEEPSEEK_R1_MODEL):
    """
    Factory function to get an LLM instance based on configured provider.
    """
    if settings.LLM_PROVIDER.lower() == "openrouter":
        return ChatOpenRouter(model_name=model_name)
    
    elif settings.LLM_PROVIDER.lower() == "openai":
        # Needs credits
        return ChatOpenAI(model_name=model_name, openai_api_key=settings.OPENAI_API_KEY.get_secret_value())
    
    # bedrock, gemini, azure, etc. can be added here in the future
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
    

# Example usage (for demonstration, remove from production code if not needed)
if __name__ == "__main__":
    llm_instance = get_llm() # Example: using a model from settings
    print(f"Instantiated LLM: {llm_instance._llm_type} with model {llm_instance.model_name}")