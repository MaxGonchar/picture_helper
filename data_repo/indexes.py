from collections.abc import Generator
from typing import TextIO
from data_repo.es import ESClient
import json


class ESIndexes:
    def __init__(self) -> None:
        self.es = ESClient()

    def get_non_system_indices(self):
        indexes = self.es.get_indexes().body
        return [i for i in indexes.split("\n") if i]
    
    def get_index_data(self, index_name: str, size: int) -> Generator[dict]:
        query = {"match_all": {}}
        sort = {"id.keyword": "asc"}
        return self.es.get_index_data(index_name, size, query, sort)

    def backup_index_data_to_file(self, index_name: str, file: TextIO, batch_size: int) -> None:
        file.writelines(
            map(
                lambda line: json.dumps(line["_source"]) + "\n",
                self.get_index_data(index_name, batch_size)
            )
        )
    
    def restore_index_data_from_file(self, index_name: str, file: TextIO) -> None:

        def data_generator():
            for line in file:
                item = json.loads(line)
                yield {
                    "_index": index_name,
                    "_id": item["id"],
                    **item
                }

        self.es.batch_index_data(data_generator())
