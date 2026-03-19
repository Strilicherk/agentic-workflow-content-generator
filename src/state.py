import operator
from typing import Annotated, TypedDict
from collections.abc import Sequence
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage

class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    materials_url: Annotated[list[str], operator.add]
    summary: Annotated[list[str], operator.add]
    draft: str