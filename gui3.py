from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
from pprint import pprint
from typing import TypedDict
import json

from flask import Flask, render_template, request, redirect, url_for

from data_repo.id import Id
from domain import Domain
from page import Page
from data_repo.images import Image, Images

MAX_PAGES_TO_HANDLE = 18
RANDOM_IDS_COUNT = MAX_PAGES_TO_HANDLE
PAGES_OK: list[Page] = []
PAGES_NOT_EXISTING: list[Page] = []

domain = Domain()
id_repo = Id(domain)
img_repo = Images(domain)

app = Flask(__name__, template_folder='.')


def get_random_ids(id_manager: Id, amount: int) -> list[str]:
    return id_manager.get_random_ids(amount)


def enrich_pages_content(attempts: int = 5) -> None:
    random_ids = get_random_ids(id_repo, RANDOM_IDS_COUNT)
    for i in range(attempts):
        pages = [Page(Domain(), id_) for id_ in random_ids]
        with ThreadPoolExecutor() as executor:
            [executor.submit(page.get_content) for page in pages]

        for page in pages:
            if page.status_code == 200:
                PAGES_OK.append(page)
            if page.status_code == 302:
                PAGES_NOT_EXISTING.append(page)
        
        print(f"Attempt {i + 1}")
        print(f"Pages OK: {len(PAGES_OK)}")
        if len(PAGES_OK) >= MAX_PAGES_TO_HANDLE:
            break

        random_ids = get_random_ids(id_repo, RANDOM_IDS_COUNT - len(PAGES_OK))


def enrich_pages_imgs() -> None:
    with ThreadPoolExecutor() as executor:
        [executor.submit(page.download_img) for page in PAGES_OK]


def parse_form(form: dict) -> dict:
    opinions = defaultdict(dict)

    for k, v in form.items():
        id_, type_ = k.split("-")
        opinions[id_][type_] = v

    return opinions


def save_imgs_data(imgs_data: list[Image]) -> None:
    print("Saving imgs data:", [img.id for img in imgs_data])
    img_repo.add_batch(imgs_data)


def delete_processed_ids(processed_ids: set) -> None:
    print("Deleting processed ids:", processed_ids)
    id_repo.delete_ids(processed_ids)


def build_img(page: Page, opinion: dict[str, str]) -> Image:
    try:
        return Image(
            id=page.id,
            tags=page.content["tags"],
            allTags=sum(page.content["tags"].values(), []),
            opinion=opinion,
            statistics=page.content["statistics"],
        )
    except KeyError:
        print("! " * 50)
        print(page.id)
        print(page.status_code)
        print(page.content)
        print("! " * 50)
        raise


def build_imgs_data(pages: list[Page], opinions: dict) -> tuple[list[Image], list]:
    imgs_data = []
    processed_ids = list()

    for page in pages:
        opinion = opinions.get(page.id)
        if opinion:
            imgs_data.append(build_img(page, opinion))
            processed_ids.append(page.id)

    return imgs_data, processed_ids


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        enrich_pages_content(attempts=10)
        enrich_pages_imgs()
        imgs = [
            {
                "id": page.id,
                "pageURL": page.url,
                "img_content": page.content.get("img_content")
            } for page in PAGES_OK
        ]
        return render_template('index3.html', imgs=imgs)
    
    if request.method == "POST":
        # if server was restarted, PAGES_OK will be empty
        if not PAGES_OK:
            return redirect(url_for('index'))

        opinions = parse_form(request.form)
        imgs_data, processed_ids = build_imgs_data(PAGES_OK, opinions)
        save_imgs_data(imgs_data)
        delete_processed_ids(processed_ids)
        PAGES_OK.clear()
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
