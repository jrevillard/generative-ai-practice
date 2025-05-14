# generative-ai-practice

# Week 2 – Local RAG App

This module focuses on building a fully local Retrieval-Augmented Generation (RAG) application using LangChain. The goal is to load documents, build a semantic index, and query a local LLM to answer user questions—all running locally.

## 📁 Structure
```
week-02_local-rag-app/
├── cli/
│   └── main.py                  # Main CLI script for querying the RAG system
├── rag/
│   ├── retriever.py             # Handles document ingestion and retrieval
│   ├── chain.py                 # Manages the LangChain QA chain
│   ├── embedder.py              # Embedding logic for documents
│   ├── llm_wrapper.py           # Wrapper for local LLM interaction
│   └── __init__.py              # Module initialization
├── configs/
│   └── settings.yaml            # Configuration file for the RAG system
├── models/                      # Directory for local models (excluded from version control)
├── documents/                   # Directory for storing input documents
├── gradio_app/
│   └── app.py                   # Gradio-based web interface for the RAG system
├── Dockerfile                   # Optional Docker environment to run everything
├── .dockerignore                # Exclude local model files from Docker context
├── README.md                    # This file
```

## 🎯 Objectives
- Build a local RAG system for document-based question answering
- Use embeddings to create a semantic index
- Query a local LLM for answers based on retrieved documents
- Provide both CLI and web-based (Gradio) interfaces for interaction
- Configure the system via YAML for flexibility

## 🚀 Quick Start

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/generative-ai-practice.git
cd generative-ai-practice/week-02_local-rag-app
```

### 2. Download a local model (Mistral or TinyLLaMA via `gguf` format)
Visit one of the following and download a compatible `.gguf` model:
- [Mistral 7B GGUF models](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)
- [TinyLLaMA GGUF models](https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF)

Place the file in a new directory:
```bash
mkdir -p models/
mv ~/Downloads/your-model-name.gguf models/
```

> **Note:** The `models/` directory is excluded from the Docker build via `.dockerignore`

### 3. Add documents for retrieval
Place your documents (PDFs, Word files, text files, etc.) in the `documents/` directory. These will be processed and indexed for retrieval.

### 4. Launch via Python (local only)
Install the required dependencies and run the CLI or Gradio app:
```bash
pip install -r requirements.txt
python cli/main.py --query "What is the GDPR?"
```

To launch the Gradio web interface:
```bash
python gradio_app/app.py
```

### OR 5. Run in Docker (recommended)
Build and run the image locally:

```bash
docker build -t local-rag-app .
docker run --rm -it -v $(pwd)/models:/app/models -v $(pwd)/documents:/app/documents -p 7860:7860 local-rag-app
```

Access the Gradio interface at `http://localhost:7860`.

## 🛠️ Configuration
Edit `configs/settings.yaml` to control the following:
- **Embedding model**: Choose a model for generating embeddings (e.g., `all-MiniLM-L6-v2`)
- **Chunk size and overlap**: Configure how documents are split into chunks
- **LLM model path**: Specify the path to your local LLM model

Example `settings.yaml`:
```yaml
embedding:
  model: all-MiniLM-L6-v2
  device: cpu
retriever:
  documents_path: "./documents"
  chunk_size: 500
  chunk_overlap: 100
llm:
  model_path: "models/mistral-7b-instruct-v0.1.Q6_K.gguf"
  n_ctx: 32768
  n_gpu_layers: 0
  temperature: 0.2
  top_p: 0.65
  repeat_penalty: 1.1
  streaming: false
  verbose: false
```

## 🧩 Components
- **Retriever**: Handles document ingestion, chunking, and retrieval using FAISS.
- **Embedder**: Generates embeddings for documents and queries.
- **LLM Wrapper**: Interfaces with the local LLM for generating answers.
- **QA Chain**: Combines retrieval and LLM interaction to answer user queries.
- **Gradio Interface**: Provides a user-friendly web interface for querying the RAG system.

## 📝 Logging and Review
All interactions and configurations are logged for debugging and review. Logs include:
- Retrieved documents
- Query embeddings
- LLM responses

## 🧪 Suggested Experiments
- 🔍 Test with different embedding models (e.g., `sentence-transformers`)
- 📄 Add new document types for ingestion (e.g., `.csv`, `.json`)
- 🧠 Experiment with different LLMs for answering queries
- ⚙️ Adjust chunk size and overlap to optimize retrieval quality
- 🌐 Customize the Gradio interface for additional features (e.g., file upload, real-time feedback)

## 📚 Resources
- [LangChain documentation](https://langchain.readthedocs.io/en/latest/)
- [FAISS documentation](https://faiss.ai/)
- [Gradio documentation](https://gradio.app/)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)

## ✅ Summary
By the end of Week 2, you should be comfortable:
- Building a local RAG system
- Configuring and using embeddings for document retrieval
- Querying a local LLM for document-based question answering
- Using both CLI and Gradio interfaces for interaction
- Running the system either natively or in Docker

This work sets the foundation for more advanced multi-modal and distributed RAG systems in future weeks.
