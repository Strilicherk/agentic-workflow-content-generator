import threading
from typing import Annotated, TypedDict
from collections.abc import Sequence
from rich import print
from rich.markdown import Markdown
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langgraph.graph import START, END, StateGraph, add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import RunnableConfig



llm = init_chat_model("llama3.2:latest", model_provider="ollama")

# 1 - State
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    # user_prompt: str
    # materials_url: Annotated[list[str], add_messages]
    # current_draft: str
    # current_review: str
    # count: int
    # last_versions: Annotated[dict[str, str], add_messages]


# 2 - Nós
def pesquisador(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}


# 3 - Builder
builder = StateGraph(
    State, context_schema=None, input_schema=State, output_schema=State
)

# 4 - Conexões
builder.add_node("pesquisador", pesquisador)
builder.add_edge(START, "pesquisador")
builder.add_edge("pesquisador", END)

# 5 - Compilar
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})

## 6 - Usar
if __name__ == '__main__':
    while True:
        user_input = input("Digite sua mensagem: ")
        if user_input.lower() in ["q", "quit"]:
            print("Bye 👋")
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke({"messages": human_message}, config=config)
        print(result["messages"][-1].content)
        print(Markdown('---'))
