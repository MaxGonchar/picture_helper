class Domain:

    def __init__(self, domain: str = "rule34.xxx") -> None:
        self.domain = domain

    def get_ids_index_prefix(self) -> str:
        return f"{'-'.join(self.domain.split('.'))}-ids"
    
    def get_imgs_index_prefix(self) -> str:
        return f"{'-'.join(self.domain.split('.'))}-imgs"

    def get_es_ids_index_name(self, id_: str) -> str:
        start, end = self._get_range_for_id(id_)
        return f"{self.get_ids_index_prefix()}-{start}-{end}"

    def get_es_imgs_index_name(self, id_: str) -> str:
        start, end = self._get_range_for_id(id_)
        return f"{self.get_imgs_index_prefix()}-{start}-{end}"

    def _get_range_for_id(self, id_: str) -> tuple[int, int]:
        try:
            int_id = int(id_)
        except ValueError:
            raise ValueError("id_ must be an integer")
        start = (int_id // 1000_000) * 1000_000
        end = start + 999_999
        return start, end

    @property
    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
        }

    def get_page_url(self, id_: str) -> str:
        return f"https://rule34.xxx/index.php?page=post&s=view&id={id_}"
