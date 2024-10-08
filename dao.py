import os
from typing import Iterator
from os.path import join
import json
from dataclasses import dataclass

import joblib
from sklearn.linear_model import LogisticRegression

from configs import (
    DATA_FOLDER,
    IMGS_FOLDER,
    TAGS_FILE,
    ID_FILE,
    MODEL_FILE,
    UNSORTED_IMGS_FILE,
    TAGS_USED_FOR_TRAINING_FILE,
)
from utils import get_img_id, generate_file_name


@dataclass
class Img:
    id: str
    tags: list[str]
    is_good: bool


class NextImgID:
    def __enter__(self):
        with open(join(DATA_FOLDER, ID_FILE), "r") as file:
            self.id = int(file.read()) + 1
        return self.id
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            with open(join(DATA_FOLDER, ID_FILE), "w") as file:
                file.write(str(self.id))
        else:
            raise exc_type(exc_val)


class ImgFile:
    def __init__(self, name: str, path: str | None = None):
        self.name = name
        self.path = join(DATA_FOLDER, IMGS_FOLDER, name) or path

    def __lt__(self, other):
        if not isinstance(other, ImgFile):
            raise TypeError("Can't compare ImgFile with other type")
        return self._num() < other._num()
    
    def __repr__(self):
        return f"ImgFile({self.name})"

    def _num(self):
        return int(self.name.split("-")[1])
    
    @property
    def content(self):
        if not os.path.exists(self.path):
            return {}

        with open(self.path, "r") as f:
            return json.load(f)
    
    @content.setter
    def content(self, content: dict):
        with open(self.path, "w") as f:
            json.dump(content, f)
        

class ImagesIterator:

    def __init__(self, files: list[ImgFile]):
        self.files = iter(sorted(files))
        self._load_images_from_next_file()

    def _load_images_from_next_file(self) -> None:
        file = next(self.files)
        self.images = iter(file.content.items())
    
    def _next_img(self) -> dict:
        id_, content = next(self.images)
        return Img(id_, content["tags"], content["isGood"])
    
    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self._next_img()
        except StopIteration:
            self._load_images_from_next_file()
            return self._next_img()


class UnsortedImages:
    def __init__(self) -> None:
        self.path = join(DATA_FOLDER, UNSORTED_IMGS_FILE)
        self.total = None
    
    def get_next(self, order_by: str | None = None) -> dict:
        with open(self.path, "r") as f:
            data = json.load(f)
        
        self.total = len(data)

        if order_by is None:
            return data[0] if data else None
        elif order_by == "likelihood":
            data = sorted(data, key=lambda x: x["likelihood"], reverse=True)
            return data[0] if data else None
        else:
            raise ValueError(f"Unknown order_by value: {order_by}")
    
    def get_n_next(self, n: int, order_by: str | None = None) -> list[dict]:
        with open(self.path, "r") as f:
            data = json.load(f)

        self.total = len(data)

        if order_by is None:
            return data[:n]
        elif order_by == "likelihood":
            data = sorted(data, key=lambda x: x["likelihood"], reverse=True)
            return data[:n]
        else:
            raise ValueError(f"Unknown order_by value: {order_by}")
    
    def delete_unsorted_image(self, img: dict):
        with open(self.path, "r") as file:
            data = json.load(file)

        data.remove(img)

        with open(self.path, "w") as file:
            json.dump(data, file)


def get_all_tags() -> list[str]:
    path = join(DATA_FOLDER, TAGS_FILE)
    with open(path, "r") as file:
        return json.load(file)


def get_tags_used_for_training() -> list[str]:
    path = join(DATA_FOLDER, TAGS_USED_FOR_TRAINING_FILE)
    with open(path, "r") as file:
        return json.load(file)


def update_tags(tags: list[str]) -> None:
    existing_tags = get_all_tags()

    for tag in tags:
        if tag not in existing_tags:
            existing_tags.append(tag)
    
    with open(join(DATA_FOLDER, TAGS_FILE), "w") as file:
        json.dump(existing_tags, file)


def save_image(img: dict):
    img_id = get_img_id(img)
    file = ImgFile(generate_file_name(int(img_id)))
    content = file.content
    content.update(img)
    file.content = content


def save_unsorted_image(img: dict):
    with open(join(DATA_FOLDER, UNSORTED_IMGS_FILE), "r") as file:
        data = json.load(file)

    data.append(img)

    with open(join(DATA_FOLDER, UNSORTED_IMGS_FILE), "w") as file:
        json.dump(data, file)


def delete_unsorted_image(img: dict):
    with open(join(DATA_FOLDER, UNSORTED_IMGS_FILE), "r") as file:
        data = json.load(file)

    data.remove(img)

    with open(join(DATA_FOLDER, UNSORTED_IMGS_FILE), "w") as file:
        json.dump(data, file)


def get_images(folder: str | None = None) -> Iterator:
    folder = folder or join(DATA_FOLDER, IMGS_FOLDER)
    files = [ImgFile(f) for f in os.listdir(folder)]
    return ImagesIterator(files)


def get_predictor() -> LogisticRegression:
    return joblib.load(join(DATA_FOLDER, MODEL_FILE))

if __name__ == "__main__":
    assert ImgFile("imgs-0-9999.json")._num() == 0
    
    assert ImgFile("imgs-0-9999.json") < ImgFile("imgs-10000-19999.json")

    f1 = ImgFile("imgs-0-9999.json")
    f2 = ImgFile("imgs-10000-19999.json")
    f3 = ImgFile("imgs-20000-29999.json")
    assert sorted([f3, f1, f2]) == [f1, f2, f3]

    # print(ImgFile("imgs-1760000-1769999.json").content)

    # i = 0
    # for img in get_images():
    #     i += 1
    #     print(img)
    #     if i == 3:
    #         break
    # print(i)
