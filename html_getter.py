# from typing import TypedDict
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


# class HTMLType(TypedDict):
#     status_code: int
#     text: str


def get_html(url: str) -> str | None:
    response = requests.get(url, headers=HEADERS, allow_redirects=False)
    if response.status_code == 200:
        return response.text
    print(f"Failed to get html from {url}, status code {response.status_code}")


# def get_html2(url: str, headers: dict[str, str]) -> HTMLType:
#     html = {"status_code": 0, "text": ""}
#     response = requests.get(url, headers=headers, allow_redirects=False)

#     if response.status_code == 200:
#         html["text"] = response.text

#     html["status_code"] = response.status_code
#     return html


# class HTMLGetter:
#     def __init__(self, url: str, headers: dict[str, str]):
#         self.url = url
#         self.headers = headers
#         self._html = ""
#         self._response_status = 0
    
#     def _get_html(self):
#         response = requests.get(self.url, headers=self.headers, allow_redirects=False)
#         self._response_status = response.status_code
#         if response.status_code == 200:
#             self._html = response.text

#     @property
#     def html(self):
#         if not self._html:
#             self._get_html()
#         return self._html
    
#     @property
#     def response_status(self):
#         if not self._response_status:
#             self._get_html()
#         return self._response_status