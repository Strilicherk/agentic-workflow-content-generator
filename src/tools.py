from ddgs import DDGS
from langchain.tools import BaseTool, tool
from rich import print


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
    print(query)

    try:
        with DDGS() as ddgs:
            resultados = ddgs.text(query, max_results=max_results)
            for resultado in resultados:
                link = resultado.get('href')
                if link:
                    urls_coletadas.append(link)
        return urls_coletadas
    except Exception as e:
        print(f"Erro na execução da ferramenta de busca: {e}")
        return e



RESEARCHER_TOOLS: list[BaseTool] = [get_urls_duckduckgo]

TOOLS: list[BaseTool] = [get_urls_duckduckgo]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}