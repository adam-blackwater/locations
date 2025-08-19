import json
from typing import Dict, Any


def extract(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_json_from_api():
    raise NotImplementedError


def extract_xml_from_file():
    raise NotImplementedError


def extract_json_from_object_storage():
    raise NotImplementedError
