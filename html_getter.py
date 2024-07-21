import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


def get_html(url: str) -> str:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text
