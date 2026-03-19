from langchain.chat_models import init_chat_model, BaseChatModel

def load_llm() -> BaseChatModel:
    return init_chat_model("llama3.2:latest", model_provider="ollama")