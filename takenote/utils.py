import json
from typing import Dict, Any


def read_json(path) -> Dict[str, Any]:
    with open(path, "r") as file:
        data = json.load(file)

    return data


def write_json(path: str, data: Dict[str, Any]):
    with open(path, "w") as file:
        json.dump(data, file, indent=3)
