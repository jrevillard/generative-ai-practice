from typing import List, Tuple

MAX_TOKENS = 3500  # Leave room for the assistant's response

class RAGChain:
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm

    def run(self, query: str, history: list = None):
        # Retrieve context documents
        context_docs = self.retriever.retrieve(query)

        # Build the prompt using the context and history
        prompt = self._build_prompt(query, context_docs, history or [])

        # DEBUG: Show the final prompt
        print("[DEBUG] Prompt sent to LLM:\n" + "-"*80)
        print(prompt)
        print("-"*80)

        # Call the LLM to generate a response
        return self.llm.complete(prompt)

    def _build_prompt(self, query: str, context_docs: list, history: list):
        history_block = "\n".join([f"User: {h['user']}\nAssistant: {h['bot']}" for h in history])
        context_block = "\n".join(context_docs)
        return f"{history_block}\n\nContext:\n{context_block}\n\nUser: {query}\nAssistant:"

# Dummy tokenizer approximation (you may replace with tiktoken or similar)
def _estimate_tokens(text: str) -> int:
    return len(text.split()) * 1.3

def build_chat_prompt(self,
    query: str,
    context_docs: list,
    history: List[Tuple[str, str]],
    prompt_format: str = "inst"  # Options: "chatml", "inst", "plain"
) -> str:
    """
    Constructs a prompt from system message, conversation history, and user input,
    using the specified prompt format. Automatically truncates older messages.
    """
    blocks = history + [("user", query)]
    prompt_parts = []
    total_tokens = 0

    def format_block(role: str, message: str) -> str:
        if prompt_format == "chatml":
            tag = {
                "system": "<|system|>",
                "user": "<|user|>",
                "assistant": "<|assistant|>"
            }.get(role, "<|user|>")
            return f"{tag}\n{message}\n"

        elif prompt_format == "inst":
            if role == "system":
                return f"<s>[INST] <<SYS>>\n{message}\n<</SYS>>\n"
            elif role == "user":
                return "[INST] " + message.strip() + " [/INST]\n"
            elif role == "assistant":
                return message.strip() + "\n"
            else:
                return message + "\n"

        elif prompt_format == "plain":
            prefix = f"{role.capitalize()}: " if role in ("user", "assistant") else ""
            return f"{prefix}{message}\n"

        else:
            raise ValueError(f"Unknown prompt format: {prompt_format}")

    # Traverse from latest to oldest to truncate correctly
    for role, message in reversed(blocks):
        formatted = format_block(role, message)
        token_count = _estimate_tokens(formatted)
        if total_tokens + token_count <= MAX_TOKENS or role == "system":
            prompt_parts.insert(0, formatted)
            total_tokens += token_count
        else:
            continue

    final_prompt = "".join(prompt_parts)
    # Add assistant marker for chatml
    if prompt_format == "chatml":
        final_prompt += "<|assistant|>\n"
    elif prompt_format == "inst":
        final_prompt = final_prompt.replace("<</SYS>>\n[INST] ", "<</SYS>>\n")

    return final_prompt.strip()