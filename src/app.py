from flask import Flask, request
from langchain_core.messages import HumanMessage
from langchain_core.runnables.config import RunnableConfig
import uuid
from graph import build_graph

app = Flask(__name__)

graph = build_graph()

@app.route('/api/agente', methods=['POST'])
def controller_agente():
    """
    Endpoint principal para interagir com o agente LangGraph.
    Espera um JSON no formato: {"mensagem": "sua pergunta", "thread_id": "opcional"}
    """
    dados = request.get_json()

    if 'mensagem' not in dados:
        return {"erro": "O corpo da requisição deve conter a chave 'mensagem'."}, 200

    user_input = dados['mensagem']
    thread_id = dados.get('thread_id', str(uuid.uuid4()))
    config = RunnableConfig(configurable={"thread_id": thread_id})

    human_message = HumanMessage(content=user_input)

    try:
        result = graph.invoke({"messages": [human_message]}, config=config)
        final_version = result.get("final_version")

        if final_version:
            resposta = final_version
            tipo_fluxo = "pesquisa_e_sintese"
        else:
            resposta = result["messages"][-1].content
            tipo_fluxo = "chat_direto"

        return {
            "thread_id": thread_id,
            "tipo_fluxo": tipo_fluxo,
            "resposta": resposta
        }, 200

    except Exception as e:
        # Captura qualquer erro não tratado no grafo para não derrubar o servidor
        return {"erro": f"Falha interna no processamento do agente: {str(e)}"}, 500


if __name__ == '__main__':
    # Roda o servidor na porta 5000
    app.run(debug=True, host='0.0.0.0', port=5000)