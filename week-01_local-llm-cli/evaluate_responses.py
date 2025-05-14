import json
import argparse
from textblob import TextBlob


def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    else:
        return "neutral"


def is_coherent(text):
    # Simple heuristic: response is coherent if it's non-empty and has proper punctuation.
    return bool(text.strip()) and any(p in text for p in ".!?")


def evaluate_log_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data:
        user_input = entry.get("user")
        model_output = entry.get("assistant")

        if model_output:
            sentiment = analyze_sentiment(model_output)
            coherent = is_coherent(model_output)

            print("User:", user_input)
            print("Assistant:", model_output)
            print("Sentiment:", sentiment)
            print("Coherent:", "✅" if coherent else "❌")
            print("=" * 40)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate model responses for sentiment and coherence.")
    parser.add_argument("--file", type=str, required=True, help="Path to the conversation log JSON file.")
    args = parser.parse_args()

    evaluate_log_file(args.file)