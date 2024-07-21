from typing import List

from bs4 import BeautifulSoup


def parse_html(html: str) -> dict:
    soup = BeautifulSoup(html, 'html.parser')
    return {
        _get_id(soup): _get_tags(soup)
    }


def _get_tags(soup: BeautifulSoup) -> List[str]:
    tags_el = soup.find("ul", {"id": "tag-sidebar"})

    tags = []
    for li in tags_el("li"):
        if li.has_attr('class') and "tag" in li['class']:
            tags.append(li("a")[1].text)
    
    return tags


def _get_id(soup: BeautifulSoup) -> str:
    stats_el = soup.find("div", {"id": "stats"})
    return stats_el.find("ul")("li")[0].text.split()[1]
