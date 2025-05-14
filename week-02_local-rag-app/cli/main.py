import typer
from typing import Annotated
from utils import load_config, initialize_components, prepare_retriever

app = typer.Typer()

@app.command()
def chat():
    """
    Interactive RAG chat session.
    """
    cfg = load_config("configs/settings.yaml")
    if not cfg:
        return

    retriever, llm, chain = initialize_components(cfg)
    if not retriever or not chain:
        return

    if not prepare_retriever(retriever):
        return

    print("💬 RAG Chat session started. Type 'exit' or 'quit' to leave.")
    chat_history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Exiting chat.")
            break

        response = chain.run(user_input)
        print(f"RAG: {response}")
        chat_history.append({"user": user_input, "bot": response})

@app.command()
def query(query: Annotated[str, typer.Argument()] = "Hello"):
    """
    Query the RAG system with a single input.
    """
    cfg = load_config("configs/settings.yaml")
    if not cfg:
        return

    retriever, llm, chain = initialize_components(cfg)
    if not retriever or not chain:
        return

    if not prepare_retriever(retriever):
        return

    print(chain.run(query))

if __name__ == "__main__":
    app()