# generative-ai-practice


# Week 1 – Local LLM CLI Assistant

This module focuses on using a local LLM (such as LLaMA.cpp or similar) via a simple command-line interface (CLI). The goal is to become familiar with prompt formatting, response evaluation, and conversation handling—all running locally.

## 📁 Structure
```
week-01_local-llm-cli/
├── cli_assistant.py             # Main CLI script for interacting with the LLM
├── prompt_templates.py          # Contains prompt variations (default, translation, summarization, sentiment)
├── conversation_logger.py       # Utility to log input/output to a JSON file
├── evaluate_responses.py        # Script to evaluate response coherence and sentiment
├── examples/
│   └── conversation_sample.json # Sample logged conversation
├── Dockerfile                   # Optional Docker environment to run everything
├── .dockerignore                # Exclude local model files from Docker context
├── README.md                    # This file
```

## 🎯 Objectives
- Interact with a local LLM through the terminal
- Structure and vary prompts for different tasks
- Log and review conversations for iterative improvement
- Evaluate the quality and sentiment of LLM outputs

## 🚀 Quick Start

### 1. Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/generative-ai-practice.git
cd generative-ai-practice/week-01_local-llm-cli
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

### 3. Launch via Python (local only)
```bash
pip install -r requirements.txt
python cli_assistant.py
```

### OR 4. Run in Docker (recommended)
Build and run the image locally:

```bash
docker build -t local-llm-cli .
docker run --rm -it -v $(pwd)/models:/app/models local-llm-cli
```

Ensure your model is in the `/models` directory mounted into the container.

## 🧩 Prompt Templates
Modify `prompt_templates.py` to control how the user query is presented to the model.

Available types:
- `default`: Plain instruction-response
- `translate`: Translate sentence to French
- `summarize`: Summarize a paragraph
- `sentiment`: Detect sentiment (positive, neutral, negative)

Example usage in `cli_assistant.py`:
```python
prompt = TEMPLATES["summarize"]("This is a long article...")
```

## 📝 Logging and Review
All assistant interactions are logged automatically via `conversation_logger.py` into a JSON file with timestamps. This can be used to:
- Track the evolution of prompt/response quality
- Build a dataset of prompts and completions

## 📊 Response Evaluation (Bonus)
Run `evaluate_responses.py` to:
- Check if responses are coherent (basic heuristics)
- Estimate sentiment polarity using `TextBlob`

This allows for light testing of the model’s reliability and tone.

## 🧪 Suggested Experiments
- 🔁 Rewrite the same question using each of the prompt types
- 🧠 Add a new template for question answering or story generation
- 🗃️ Save and analyze a complete 10-message conversation
- 🔎 Use `TextBlob` on the response to refine prompt clarity

## 📚 Resources
- [TextBlob documentation](https://textblob.readthedocs.io/en/dev/)
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- [OpenLLM Leaderboard](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)

## ✅ Summary
By the end of Week 1, you should be comfortable:
- Using LLMs locally from a CLI interface
- Experimenting with prompt structure
- Logging and evaluating assistant responses
- Using either native Python or Docker-based workflow

The work done here prepares you to build more complex applications like Retrieval-Augmented Generation (RAG) and multi-modal agents in the following weeks.
