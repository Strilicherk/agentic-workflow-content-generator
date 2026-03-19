from state import State
from utils import load_llm
from __init__ import llm
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import RunnableConfig

def call_llm(state: State) -> State:
    result = load_llm().invoke(state["messages"])
    return {"messages": [result]}

def researcher(state: State) -> State:
    call_llm()

def build_graph() -> CompiledStateGraph[State, None, State, State]:
    builder = StateGraph(State)

    builder.add_node("call_llm", call_llm)
    
    builder.add_edge(START, "call_llm")
    builder.add_edge("call_llm", END)

    return builder.compile(checkpointer=InMemorySaver())




