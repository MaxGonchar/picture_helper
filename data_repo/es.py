from collections.abc import Generator, Iterable

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# TODO: Move to configs
ES_HOST = "http://localhost:9200"


class ESClient:

    def __init__(self) -> None:
        self.es = Elasticsearch(hosts=[ES_HOST])

    def index_doc(self, index: str, id_: str, doc: dict) -> None:
        self.es.index(index=index, id=id_, body=doc)

    def get_indexes(self):
        return self.es.cat.indices(index='*,-.*', h='index')

    def create_index(self, index_name: str):
        self.es.indices.create(index=index_name)

    def get_index_data(self, index_name: str, size: int, query: dict, sort: dict | None = None) -> Generator[dict]:
        search_query = {
            "index": index_name,
            "size": size,
            "query": query
        }

        if sort:
            search_query["sort"] = sort

        response = self.es.search(**search_query)
        hits = response["hits"]["hits"]

        while hits:
            yield from hits
            search_query["search_after"] = hits[-1]["sort"]
            response = self.es.search(**search_query)
            hits = response["hits"]["hits"]

    def batch_index_data(self, data: Iterable) -> None:
        bulk(self.es, data)

    def get_random_doc(self, index: str, amount: int) -> dict:
        return self.es.search(
            index=index,
            body={
                "size": amount,
                "query": {
                    "function_score": {
                        "random_score": {}
                    }
                }
            })["hits"]["hits"]

    def delete_doc(self, index: str, id_: str) -> None:
        self.es.delete(index=index, id=id_)

    def delete_by_query(self, index: str, query: dict) -> None:
        self.es.delete_by_query(index=index, body=query)
