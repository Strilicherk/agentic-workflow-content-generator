from graph import build_graph
import threading
from rich import print
from rich.markdown import Markdown
from langchain_core.messages import HumanMessage
from langgraph.graph.state import RunnableConfig

def main() -> None:
    config = RunnableConfig(configurable={"thread_id": threading.get_ident()})
    graph = build_graph()
    
    while True:
        user_input = input("Digite sua mensagem: ")
        if user_input.lower() in ["q", "quit"]:
            print("Bye 👋")
            break

        human_message = HumanMessage(user_input)
        
        result = graph.invoke({"messages": human_message}, config=config)
        print(Markdown('---'))
        print(result["final_version"])
        print(Markdown('---'))

if __name__ == '__main__':
    main()
