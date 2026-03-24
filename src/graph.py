from nodes import researcher_node, scraper_node, synthesizer_node
from tools import RESEARCHER_TOOLS
from routers import router
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from state import State
from langgraph.prebuilt import ToolNode

def build_graph() -> CompiledStateGraph[State, None, State, State]:
    builder = StateGraph(State)

    # Definição dos nós
    builder.add_node("researcher_node", researcher_node)
    builder.add_node("researcher_tools_node", ToolNode(tools=RESEARCHER_TOOLS))
    builder.add_node("scraper_node", scraper_node)
    builder.add_node("synthesizer_node", synthesizer_node)

    builder.add_edge(START, "researcher_node")
    
    builder.add_conditional_edges(
        "researcher_node", 
        router, 
        ['researcher_tools_node', 'scraper_node', '__end__']
    )

    builder.add_edge("researcher_tools_node", "researcher_node")
    builder.add_edge("scraper_node", "synthesizer_node")
    builder.add_edge("synthesizer_node", END)
    
    return builder.compile(checkpointer=InMemorySaver())




