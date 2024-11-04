from collections import defaultdict

from bs4 import BeautifulSoup

from ph_types import ParsedImgType


def parse_html(html: str) -> ParsedImgType:
    soup = BeautifulSoup(html, 'html.parser')
    return {
        "id": _get_id(soup),
        "tags": _get_tags(soup),
        "imgUrl": _get_img_url(soup),
        "statistics": _parse_statistics(soup)
    }


def _get_tags(soup: BeautifulSoup) -> dict[str, list[str]]:
    tags_el = soup.find("ul", {"id": "tag-sidebar"})

    tags = defaultdict(list)
    for li in tags_el("li"):
        if li.has_attr('class') and "tag" in li['class']:
            tags[li['class'][0].split("-")[-1]].append(li("a")[1].text)
    
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


def _parse_statistics(soup: BeautifulSoup) -> dict:
    statistics = {}
    statistics_ul = soup.find("div", {"id": "stats"}).find("ul")

    for li in statistics_ul("li"):

        if li.text.strip().startswith("Posted"):
            statistics["posted"] = "T".join(li.text.strip().split()[1:3])
            statistics["posted_by"] = {
                "name": li("a")[0].text.strip(),
                "url": li("a")[0]["href"]
            }

        if li.text.strip().startswith("Source"):
            if li("a"):  # source not always present as a link
                statistics["source"] = li("a")[0]["href"]
            elif len(li.text.strip().split(maxsplit=1)) > 1:  # source can be empty
                statistics["source"] = li.text.strip().split(maxsplit=1)[-1]
            else:
                statistics["source"] = "Unknown"

    return statistics
