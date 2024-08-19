from dataclasses import dataclass
from data_repo.es import ESClient


@dataclass
class Image():
    id: int
    tags: list[str]
    isGood: bool


class Images:

    def __init__(self) -> None:
        self.es = ESClient()

    def add(self, image: Image) -> None:
        doc = {
            "id": image.id,
            "tags": image.tags,
            "tagsNumber": len(image.tags),
            "isGood": image.isGood
        }
        index = self.generate_index(image.id)
        self.es.index(index, image.id, doc)

    def __iter__(self):
        ...

    def __next__(self):
        ...
    
    @staticmethod
    def generate_index(id_: int) -> str:
        start = (id_ // 1000_000) * 1000_000
        end = start + 999_999
        return f"imgs-{start}-{end}"