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
