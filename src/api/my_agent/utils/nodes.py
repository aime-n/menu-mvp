from src.api.utils.llm_factory import get_llm
from src.api.my_agent.utils.state import State
from src.api.core.config import settings


llm = get_llm(settings.DEEPSEEK_V3_MODEL)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
