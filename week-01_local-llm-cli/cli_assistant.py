import os
from llama_cpp import Llama
from typing import List, Tuple
from prompt_templates import TEMPLATES
from conversation_logger import log_interaction
from models import MODELS, MODEL_PROMPT_FORMATS
import argparse

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="CLI Assistant with a local LLM")
    parser.add_argument("--mode", type=str, default="default", help="Template to use for the prompt. Available templates: {', '.join(TEMPLATES.keys())}")
    parser.add_argument("--model", type=str, default="mistral", help=f"Model to use. Available models: {', '.join(MODELS.keys())}")
    parser.add_argument("--temperature", type=float, default=0.1, help="Sampling temperature for the model (higher = more random)")
    parser.add_argument("--top_p", type=float, default=0.5, help="Nucleus sampling probability (higher = more diverse)")
    parser.add_argument("--system", type=str, default="You are a helpful assistant.", help="System message to steer the assistant's behavior")
    args, unknown = parser.parse_known_args()
    return args

def get_prompt(mode, user_input, system_message, prompt_format, context: List[Tuple[str, str]] = None):
    """Retrieve the prompt template based on the mode and format it for the model."""

    mode_prompt = TEMPLATES[mode](history=context, current_input=user_input, system_message=system_message, prompt_format=prompt_format)

    return mode_prompt

def chat_loop():
    """Main chat loop for the CLI assistant."""
    args = parse_arguments()

    # Validate the mode
    if args.mode not in TEMPLATES:
        print(f"Error: Mode '{args.mode}' not recognized. Available modes: {', '.join(TEMPLATES.keys())}")
        return

    # Get the model path from the MODELS dictionary
    if args.model not in MODELS:
        print(f"Error: Model '{args.model}' not recognized. Available models: {', '.join(MODELS.keys())}")
        return
    
    # Get the model prompt format from the MODEL_PROMPT_FORMATS dictionary
    if args.model not in MODEL_PROMPT_FORMATS:
        print(f"Error: Model '{args.model}' not recognized in the prompt format list. Available models: {', '.join(MODEL_PROMPT_FORMATS.keys())}")
        return

    model_path = MODELS[args.model]
    prompt_format = MODEL_PROMPT_FORMATS[args.model]

    # Check if the model file exists
    if not os.path.exists(model_path):
        print(f"Error: Model file not found at {model_path}")
        return

    print("\n🔹 Welcome to your CLI Assistant (Local LLM)")
    print("Type 'exit' to quit.\n")
    print(f"Using model: {args.model} ({model_path})")
    print(f"Using mode: {args.mode}")
    print(f"Temperature: {args.temperature}")
    print(f"Top P: {args.top_p}")
    print(f"System message: {args.system}\n")


    # Initialize the model with the specified path
    llm = Llama(model_path=model_path, n_ctx=2048, n_threads=6, n_gpu_layers=0, verbose=False)

    # Initialize conversation context
    context:List[Tuple[str, str]] = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("\n👋 Goodbye.")
            break

        # Generate the prompt
        prompt = get_prompt(args.mode, user_input, context=context, system_message=args.system, prompt_format=prompt_format)
        if user_input is None or user_input.strip() == "":
            continue

        # Display the prompt preview
        print("\n[Prompt Preview]")
        print(prompt)
        print("\n[Generating Response...]\n")

        # Generate the response
        response = llm(prompt, max_tokens=2048, temperature=args.temperature, top_p=args.top_p, stop=["###"])
        answer = response["choices"][0]["text"].strip()

        # Log the interaction
        log_interaction(user_input, answer)

        # Add to context for multi-turn conversation
        context.append(("user", user_input))
        context.append(("assistant", answer))

        # Display the assistant's response
        print(f"Assistant: {answer}\n")

if __name__ == "__main__":
    chat_loop()

