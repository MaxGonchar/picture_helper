import base64
import requests

from domain import Domain
from html_parser import parse_html


class Page:
    def __init__(self, domain: Domain, id_: str) -> None:
        self.domain = domain
        self.id = id_
        self.status_code = 0
        self.content = {}

        self.url = self.domain.get_page_url(self.id)
    
    def enrich(self) -> None:
        self._get_html()

    def get_content(self) -> None:
        response = requests.get(self.url, headers=self.domain.headers, allow_redirects=False)
        self.status_code = response.status_code
        if response.status_code == 200:
            self.content = parse_html(response.text)
    
    def download_img(self) -> None:
        if self.content["imgUrl"]:
            response = requests.get(self.content["imgUrl"], headers=self.domain.headers, timeout=10)
            self.content["img_content"] = response.content
            self.content["img_content"] = base64.b64encode(response.content).decode('utf-8')
