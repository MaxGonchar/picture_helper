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
        index = self.generate_index_name(image.id)
        self.es.index_doc(index, image.id, doc)

    @staticmethod
    def generate_index_name(id_: int) -> str:
        start = (id_ // 1000_000) * 1000_000
        end = start + 999_999
        return f"imgs-{start}-{end}"