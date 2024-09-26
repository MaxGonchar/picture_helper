from data_repo.es import ESClient
from domain import Domain


class Id:
    def __init__(self, domain: Domain) -> None:
        self.es = ESClient()
        self.domain = domain
    
    def add_id(self, id_: str) -> None:
        body = {"id": id_, "domain": self.domain.domain}
        index = self.domain.get_es_ids_index_name(id_)
        self.es.index_doc(index, id_, body)
    
    def add_ids(self, ids: list[str]) -> None:
        ids_data = ({
            "_index": self.domain.get_es_ids_index_name(id_),
            "_id": id_,
            "id": id_,
            "domain": self.domain.domain
        } for id_ in ids)
        self.es.batch_index_data(ids_data)
    
    def get_random_id(self) -> str:
        return self.es.get_random_doc(
            f"{self.domain.get_ids_index_prefix()}*"
        )
    
    def delete_id(self, id_: str) -> None:
        self.es.delete_doc(
            self.domain.get_es_ids_index_name(id_),
            id_
        )


class NextShuffledImgID:
    def __init__(self, domain: Domain) -> None:
        self.id_manager = Id(domain)

    def __enter__(self):
        self.id = self.id_manager.get_random_id()["id"]
        return self.id
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.id_manager.delete_id(self.id)
        else:
            raise exc_type(exc_val)
