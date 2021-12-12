import json


def json_loader(path: str):
    with open(path, "r", encoding='utf-8') as f:
        data = json.load(f)
    return data
