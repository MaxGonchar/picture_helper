from typing import TypedDict


class ParsedImgType(TypedDict):
    id: str
    tags: list[str]
    imgUrl: str


class UnsortedImgType(TypedDict):
    id: str
    tags: list[str]
    imgUrl: str
