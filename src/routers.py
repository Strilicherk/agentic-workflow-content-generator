from state import State
from typing import Literal
from rich import print
from langgraph.types import Send
from prompts import SCRAPER_SYSTEM_PROMPT
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

def router(state: State) -> Literal["researcher_tools_node","scraper_node", "__end__"]:
    print(">router \n")

    llm_response = state["messages"][-1]

    if getattr(llm_response, 'tool_calls', None):
        return "researcher_tools_node"
    elif len(state["materials_url_list"]) > 0:
        urls = state['materials_url_list']
        rotas_paralelas = []
        for url in urls:
            rotas_paralelas.append(Send(
                "scraper_node", 
                {
                    "messages": [SystemMessage(SCRAPER_SYSTEM_PROMPT)] + state["messages"],
                    "url": url
                }))
        return rotas_paralelas
    return "__end__"