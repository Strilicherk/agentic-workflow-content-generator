from langchain.chat_models import init_chat_model, BaseChatModel
import os
from rich import print
from langchain_community.document_loaders import WebBaseLoader
from bs4 import SoupStrainer

def load_llm() -> BaseChatModel:
    return init_chat_model("llama3.2:latest", model_provider="ollama")

def limpar_texto(texto_bruto: str) -> str:
    """
    Recebe uma string com excesso de \n e espaços vazios e retorna um texto limpo.
    """

    linhas = texto_bruto.splitlines()
    linhas_sem_espacos = [linha.strip() for linha in linhas]
    linhas_validas = [linha for linha in linhas_sem_espacos if linha]
    texto_limpo = "\n".join(linhas_validas)
    
    return texto_limpo

def web_scraping(url: str) -> str:
    os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

    loader = WebBaseLoader(
        web_paths=[url],
        bs_kwargs={"parse_only": SoupStrainer("p")}
    )

    docs = loader.load()

    if docs:
        texto_final = limpar_texto(docs[0].page_content)
        return texto_final
    else:
        print("Nenhum conteúdo encontrado.")
        return "Nenhum conteúdo encontrado."