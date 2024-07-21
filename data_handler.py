import json
from typing import List, Dict


def _read_data(file: str = "data.json"):
    with open(file, "r") as f:
        data = json.loads(f.read())
    return data


def _write_data(data: dict, file: str = "data.json"):
    with open(file, "w") as f:
        f.write(json.dumps(data, indent=2))


def update_data(img_data: Dict[str, List[str]], is_good: bool):
    img_id, img_tags = list(img_data.items())[0]
    data = _read_data()
    
    data["tags"] = list(set(data["tags"]) | set(img_tags))  
    img_obj = {
        "tags": img_tags,
        "isGood": is_good
    }
    data["imgs"][img_id] = img_obj

    _write_data(data)
