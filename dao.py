import os
from typing import Iterator
from os.path import join
import json
from dataclasses import dataclass

DATA_FOLDER = "data"
IMGS_FOLDER = "images"
TAGS_FILE = "tags.json"


@dataclass
class Img:
    id: str
    tags: list[str]
    is_good: bool


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


def get_all_tags() -> list[str]:
    path = join(DATA_FOLDER, TAGS_FILE)
    with open(path, "r") as file:
        return json.load(file)


def save_image(img: dict):
    pass


def save_unsorted_image(img: dict):
    pass


def get_images(folder: str | None = None) -> Iterator:
    folder = folder or join(DATA_FOLDER, IMGS_FOLDER)
    files = [ImgFile(f) for f in os.listdir(folder)]
    return ImagesIterator(files)

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
