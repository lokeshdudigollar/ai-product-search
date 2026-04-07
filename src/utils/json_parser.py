import json


def safe_json_loads(text: str, default):
    try:
        return json.loads(text)
    except Exception:
        return default