
from bs4 import BeautifulSoup

from ph_types import ParsedImgType


def parse_html(html: str) -> ParsedImgType:
    soup = BeautifulSoup(html, 'html.parser')
    return {
        "id": _get_id(soup),
        "tags": _get_tags(soup),
        "imgUrl": _get_img_url(soup),
        "isVideo": _is_video(soup),
    }


def _get_tags(soup: BeautifulSoup) -> list[str]:
    tags_el = soup.find("ul", {"id": "tag-sidebar"})

    tags = []
    for li in tags_el("li"):
        if li.has_attr('class') and "tag" in li['class']:
            tags.append(li("a")[1].text)
    
    return tags


def _get_id(soup: BeautifulSoup) -> str:
    stats_el = soup.find("div", {"id": "stats"})
    return stats_el.find("ul")("li")[0].text.split()[1]


def _get_img_url(soup: BeautifulSoup) -> str:
    img_el = soup.find("img", {"id": "image"})
    if img_el:
        return img_el["src"]


def _is_video(soup: BeautifulSoup) -> bool:
    return bool(soup.find("video"))
