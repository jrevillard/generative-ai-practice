# Week 3 - OpenVINO Optimization & LLM Integration

This module combines performance optimization with OpenVINO/ONNX and implements two AI applications: an LLM-powered chatbot and a RAG system using LangChain.

## 📁 Structure
```
week-03_openvino-tests/
├── Dockerfile                   # Container setup with OpenVINO
├── requirements.txt             # Core dependencies
├── requirements_cpu.txt         # Intel-optimized packages
├── notebooks/
│   ├── 01-openvino_benchmark.ipynb    # Performance comparison
│   ├── 02-llm-chatbot.ipynb           # Optimized chatbot with Mistral/LLaMA
│   ├── 03-llm-rag-langchain.ipynb     # RAG pipeline with OpenVINO
│   └── onnx_to_openvino_benchmark.ipynb  # Model conversion guide
└── models/                      # Local models directory
```

## 🎯 Key Objectives
1. Benchmark ONNX vs OpenVINO inference performance
2. Optimize LLMs for Intel hardware
3. Implement a production-ready chatbot
4. Build RAG system with LangChain integration
5. Document model conversion best practices

## 🚀 Getting Started

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/generative-ai-practice.git
cd week-03_openvino-tests && pip install -r requirements_cpu.txt && pip install -r requirements.txt
```

### 2. Launch Applications
**Chatbot:**
```bash
jupyter notebook notebooks/02-llm-chatbot.ipynb
```

**RAG System:**
```bash
jupyter notebook notebooks/03-llm-rag-langchain.ipynb
```

## ⚡ Key Features

### LLM Chatbot Optimization
```python
from openvino.runtime import Core

# Load and optimize LLM
core = Core()
llm_model = core.read_model("mistral-7b.xml")
llm = core.compile_model(llm_model, "CPU")

# Chat interface
def generate_response(prompt):
    return llm.infer_new_request({"prompt": prompt})
```

### RAG with LangChain
```python
from langchain.chains import RetrievalQA
from rag.retriever import OpenVINORetriever

retriever = OpenVINORetriever(
    model_path="retriever.xml",
    document_store="knowledge_base/"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=optimized_llm,
    chain_type="stuff",
    retriever=retriever
)
```

## 📚 Resources
- [OpenVINO LLM Guide](https://docs.openvino.ai/nightly/llm_docs.html)
- [LangChain RAG Documentation](https://python.langchain.com/docs/use_cases/question_answering/)
- [ONNX Runtime Optimization](https://onnxruntime.ai/docs/performance/tune-performance.html)
