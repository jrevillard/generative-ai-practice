import json
from datetime import datetime, timezone

def log_interaction(user_input, response_text, path="examples/conversation_log.json"):
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": user_input,
        "assistant": response_text
    }
    try:
        with open(path, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    except FileNotFoundError:
        data = []

    data.append(entry)

    with open(path, "w") as file:
        json.dump(data, file, indent=2)
