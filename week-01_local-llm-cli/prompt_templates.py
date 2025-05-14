from typing import List, Tuple

MAX_TOKENS = 3500  # Leave room for the assistant's response

# Dummy tokenizer approximation (you may replace with tiktoken or similar)
def estimate_tokens(text: str) -> int:
    return len(text.split()) * 1.3

def build_chat_prompt(
    history: List[Tuple[str, str]],
    current_input: str,
    system_message: str = "You are a helpful assistant.",
    prompt_format: str = "chatml"  # Options: "chatml", "inst", "plain"
) -> str:
    """
    Constructs a prompt from system message, conversation history, and user input,
    using the specified prompt format. Automatically truncates older messages.
    """
    blocks = [("system", system_message)] + history + [("user", current_input)]
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
        token_count = estimate_tokens(formatted)
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

# Optional: static prompt examples for other modes
def translate_prompt(current_input, system_message, prompt_format, history=[]):
    return build_chat_prompt(history, f"Translate the following sentence to French:\n{current_input}", system_message, prompt_format)

def summarize_prompt(current_input, system_message, prompt_format, history=[]):
    return build_chat_prompt(history, f"Summarize this content:\n{current_input}", system_message, prompt_format)

def sentiment_prompt(current_input, system_message, prompt_format, history=[]):
    return build_chat_prompt(history, f"What is the sentiment of the following message?\n{current_input}", system_message, prompt_format)

TEMPLATES = {
    "default": build_chat_prompt,
    "translate": translate_prompt,
    "summarize": summarize_prompt,
    "sentiment": sentiment_prompt
}
