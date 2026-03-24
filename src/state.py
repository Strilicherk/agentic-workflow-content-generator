import operator
from typing import Annotated, TypedDict
from collections.abc import Sequence
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage


class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    materials_url_list: Annotated[list[str], operator.add]
    draft_list: Annotated[list[str], operator.add]
    final_version: str

# class UrlList(TypedDict):
#     url: str
#     status: bool

class ScraperState(TypedDict):
    messages: list[BaseMessage]
    url: str