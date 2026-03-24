from state import State, ScraperState
from prompts import RESEARCH_SYSTEM_PROMPT, SYNTHESIZER_SYSTEM_PROMPT
from utils import load_llm, web_scraping
from tools import RESEARCHER_TOOLS
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langgraph.prebuilt import ToolNode
from rich import print
from rich.markdown import Markdown
import json

def researcher_node(state: State) -> State:
    try:
        if isinstance(state["messages"][-1], ToolMessage):
            try:
                urls = json.loads(state["messages"][-1].content)
                print(f"URLs armazenadas com sucesso: {urls}")
                Markdown('---')
                return {"materials_url_list": urls}
            except json.JSONDecodeError as e:
                print(f"[ERRO DE PARSING] Falha ao decodificar URLs: {e}")
                Markdown('---')
                return {"materials_url_list": []} 
        
        llm_with_tools = load_llm().bind_tools(RESEARCHER_TOOLS)
        messages_with_system_prompt = [SystemMessage(content=RESEARCH_SYSTEM_PROMPT)] + state["messages"]
        llm_response = llm_with_tools.invoke(messages_with_system_prompt)
        
        return {"messages": llm_response}

    except Exception as e:
        print(f"[ERRO FATAL - RESEARCHER] {e}")
        Markdown('---')
        return {"messages": AIMessage(content="Ocorreu um erro interno durante a pesquisa das fontes.")}

def scraper_node(state: ScraperState) -> dict:
    url_alvo = state.get("url", "URL_DESCONHECIDA")

    try:
        raw_text = web_scraping(url_alvo)
        formatted_content = f"""Aqui está o conteúdo extraído da URL solicitada. Analise este conteúdo para gerar o seu resumo:
<texto_do_site>
{raw_text}
</texto_do_site>"""
        print(f"Texto cru extraido com sucesso: \n {formatted_content}")
        Markdown('---')

        llm_response = load_llm().invoke(state["messages"] + [HumanMessage(content=formatted_content)])
        print(f"Resumo gerado: \n {llm_response}")
        Markdown('---')
        
        return {"draft_list": [llm_response.content]}

    except Exception as e:
        print(f"[ERRO NO SCRAPER] Falha ao processar a URL {url_alvo}: {e}")
        Markdown('---')
        mensagem_erro = f"[FALHA DE EXTRAÇÃO] Não foi possível obter ou resumir os dados da URL: {url_alvo} devido a um erro de conexão."
        return {"draft_list": [mensagem_erro]}

def synthesizer_node(state: State) -> dict:
    try:
        drafts = state.get("draft_list", [])
        if not drafts:
            drafts_combined = "Nenhum material de apoio foi extraído com sucesso pelas ferramentas."
        else:
            drafts_combined = "\n\n---\n\n".join(drafts)
            
        prompt = [SystemMessage(content=SYNTHESIZER_SYSTEM_PROMPT)] + state["messages"] + [HumanMessage(content=drafts_combined)]

        llm_response = load_llm().invoke(prompt)
        print(f"Versão Final: \n {llm_response}")
        Markdown('---')
        return {"final_version": llm_response.content}

    except Exception as e:
        print(f"[ERRO NO SYNTHESIZER] {e}")
        return {"final_version": "Não foi possível consolidar a resposta final devido a um erro de processamento."}

researcher_tools_node = ToolNode(tools=RESEARCHER_TOOLS)