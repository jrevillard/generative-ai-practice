MODELS = {
    "mistral": "models/mistral-7b-instruct-v0.1.Q6_K.gguf",
    "tinyllama": "models/tinyllama-1.1b-chat-v1.0.Q6_K.gguf",
}


# plain : no formating
# chatml: <|system|>, <|user|>, <|assistant|>
# inst   : [INST]...[/INST]
MODEL_PROMPT_FORMATS = {
    "mistral": "inst",
    "tinyllama": "plain",
}