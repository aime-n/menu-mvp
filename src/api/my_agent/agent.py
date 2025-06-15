from langgraph.graph import StateGraph, START
from src.api.my_agent.utils.state import State
from src.api.my_agent.utils.nodes import chatbot

from src.api.utils.visualize_graph import visualize_graph
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)


# entry point for the graph
graph_builder.add_edge(START, "chatbot")

# compile the graph
graph = graph_builder.compile()

visualize_graph(graph, save=True, filename="graph.png")


if __name__ == "__main__":
    print("Graph compiled and saved as graph.png")
    result = graph.invoke({"messages": ["Hello, how are you?"]})
    print(result)