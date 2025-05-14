from langchain_community.llms import LlamaCpp
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class LLMWrapper:
    def __init__(self, config: dict):
        """
        Initialize a local GGUF-based LLM using llama-cpp and configuration dictionary.
        """
        model_path = config["model_path"]
        callbacks = [StreamingStdOutCallbackHandler()] if config.get("streaming", False) else None

        self.llm = LlamaCpp(
            model_path=model_path,
            n_ctx=config.get("n_ctx", 2048),
            n_gpu_layers=config.get("n_gpu_layers", 0),
            temperature=config.get("temperature", 0.7),
            top_p=config.get("top_p", 0.95),
            repeat_penalty=config.get("repeat_penalty", 1.1),
            streaming=config.get("streaming", False),
            callbacks=callbacks,
            verbose=config.get("verbose", False)
        )

    def complete(self, prompt: str, max_new_tokens: int = 512) -> str:
        return self.llm.invoke(prompt)