import gradio as gr
from utils import load_config, initialize_components, prepare_retriever

# Chargement de la config
cfg = load_config("configs/settings.yaml")
if not cfg:
    raise RuntimeError("Configuration file not found or invalid.")

# Initialisation du pipeline
retriever, llm, chain = initialize_components(cfg)
if not retriever or not chain:
    raise RuntimeError("Failed to initialize components.")

if not prepare_retriever(retriever):
    raise RuntimeError("Failed to load documents.")

chat_history = []

def chat(query):
    global chat_history
    response = chain.run(query, history=chat_history)
    context_docs = retriever.retrieve(query)
    chat_history.append({"user": query, "bot": response})

    return (
        response,
        "\n---\n".join(context_docs),
        chain._build_prompt(query, context_docs, chat_history[:-1])
    )

# UI Gradio
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Local RAG Chatbot with Mistral + FAISS")
    with gr.Row():
        input_box = gr.Textbox(label="Your question", interactive=True, submit_btn="Ask")
    with gr.Row():
        output_box = gr.Textbox(label="LLM Response", lines=5)
    with gr.Row():
        prompt_box = gr.Textbox(label="Full Prompt Sent to LLM", lines=15)

    input_box.submit(fn=chat, inputs=input_box, outputs=[output_box, prompt_box],)

if __name__ == "__main__":
    demo.launch()