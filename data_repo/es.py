from typing import TypedDict

from elasticsearch import Elasticsearch

# TODO: Move to configs
ES_HOST = "http://localhost:9200"

class ESImageDoc(TypedDict):
    id: int
    tags: list[str]
    tagsNumber: int
    isGood: bool


class ESClient:

    def __init__(self) -> None:
        self.es = Elasticsearch(hosts=[ES_HOST])

    def index(self, index: str, id_: int, doc: ESImageDoc):
        self.es.index(index=index, id=id_, body=doc)
