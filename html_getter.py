import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
}


def get_html(url: str) -> str | None:
    response = requests.get(url, headers=headers, allow_redirects=False)
    if response.status_code == 200:
        return response.text
    print(f"Failed to get html from {url}, status code {response.status_code}")
