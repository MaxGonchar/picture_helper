from data_repo.es import ESClient


class Domain:
    def __init__(self, domain: str = "rule34.xxx") -> None:
        self.domain = domain
    
    def get_ids_index_prefix(self) -> str:
        return f"{'-'.join(self.domain.split('.'))}-ids"
    
    def get_es_ids_index_name(self, id_: str) -> str:
        try:
            int_id = int(id_)
        except ValueError:
            raise ValueError("id_ must be an integer")
        start = (int_id // 1000_000) * 1000_000
        end = start + 999_999
        return f"{self.get_ids_index_prefix()}-{start}-{end}"


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
