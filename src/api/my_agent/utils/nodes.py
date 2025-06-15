from src.api.utils.llm_factory import get_llm
from src.api.my_agent.utils.state import State


llm = get_llm()

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
