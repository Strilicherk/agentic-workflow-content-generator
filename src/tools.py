from ddgs import DDGS
from langchain.chat_models import init_chat_model
from langchain.tools import BaseTool, tool
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from pydantic import ValidationError
from rich import print

llm = init_chat_model("llama3.2:latest", model_provider="ollama")

@tool
def get_urls_duckduckgo(query: str) -> list[str]:
    """
    Realiza uma busca no DuckDuckGo e extrai as URLs dos resultados.
    
    Parâmetros:
        query (str): O tema ou termo de pesquisa.
        
    Retorno:
        list[str]: Uma lista contendo apenas as URLs encontradas.
    """
    urls_coletadas = []
    max_results = 5

    try:
        # O DDGS é inicializado com um gerenciador de contexto (with) 
        # para garantir o fechamento adequado de conexões de rede.
        with DDGS() as ddgs:
            # O método .text retorna um gerador contendo dicionários com os resultados
            resultados = ddgs.text(query, max_results=max_results)
            
            for resultado in resultados:
                # Extraímos apenas a chave 'href', que contém o link direto para o site
                link = resultado.get('href')
                if link:
                    urls_coletadas.append(link)
                    
        return urls_coletadas
    except Exception as e:
        print(f"Erro na execução da ferramenta de busca: {e}")
        return e

# Definindo a instrução da IA, uma mensagem do usuário e passando isso como contexto.
system_message = SystemMessage(
    "You are a helpful assistant. You have access to tools. When the user asks "
    "for something, first look if you have a tool that solves that problem."
    "Remember, you do not have to always use the tool, wait for the user to request for a research, if the user just say something random, you do not need to use it."
)
human_message = HumanMessage(
    "Bom dia!."
)
messages: list[BaseMessage] = [system_message, human_message]

# Definindo as ferramentas
tools: list[BaseTool] = [get_urls_duckduckgo]
tools_by_name = {tool.name: tool for tool in tools}

# Agora chamamos a llm porém passando as ferramentas
llm_with_tools = llm.bind_tools(tools)
llm_response = llm_with_tools.invoke(messages)
messages.append(llm_response)

# Verificamos se o modelo tenta chamar algo
if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls"):
    call = llm_response.tool_calls[-1]
    id_, name, args = call["id"], call["name"], call["args"]

    try:
        content = tools_by_name[name].invoke(args)
        status = "success"
    except (KeyError, IndexError, TypeError, ValidationError, ValueError) as error:
        content = f"Please, fix your mistakes: {error}"
        status = "error"

    tool_message = ToolMessage(content=content, tool_call_id = id_, status=status)
    messages.append(tool_message)

    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)

print(messages)

    