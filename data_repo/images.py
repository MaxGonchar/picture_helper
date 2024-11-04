from dataclasses import dataclass
from data_repo.es import ESClient
from domain import Domain


# @dataclass
# class Image():
#     id: int
#     tags: list[str]
#     isGood: bool

@dataclass
class Image():
    id: str
    tags: dict
    allTags: list[str]
    opinion: list[str]
    statistics: dict


class Images:

    def __init__(self, domain: Domain) -> None:
        self.es = ESClient()
        self.domain = domain
    
    def add_batch(self, images: list[Image]) -> None:
        images_data = ({
            "_index": self.domain.get_es_imgs_index_name(image.id),
            "_id": image.id,
            "id": image.id,
            "tags": image.tags,
            "allTags": image.allTags,
            "opinion": image.opinion,
            "statistics": image.statistics,
        } for image in images)
        self.es.batch_index_data(images_data)

    # def add(self, image: Image) -> None:
    #     doc = {
    #         "id": image.id,
    #         "tags": image.tags,
    #         "tagsNumber": len(image.tags),
    #         "isGood": image.isGood
    #     }
    #     index = self.generate_index_name(image.id)
    #     self.es.index_doc(index, image.id, doc)

    # @staticmethod
    # def generate_index_name(id_: int) -> str:
    #     start = (id_ // 1000_000) * 1000_000
    #     end = start + 999_999
    #     return f"imgs-{start}-{end}"