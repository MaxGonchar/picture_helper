from copy import deepcopy
import base64
from flask import Flask, render_template, request, session, redirect, url_for
import requests

from configs import URL
from dao import UnsortedImages, delete_unsorted_image, save_image, update_tags
from ph_types import UnsortedImgType
from html_getter import HEADERS

app = Flask(__name__, template_folder='.')
app.secret_key = b'sjdhajhdkjahskdjhakjshdkajhsdkjahskjdh'


def prepare_sorted_img(unsorted_image: UnsortedImgType, is_good: bool, opinion: str) -> dict:
    img = {
        unsorted_image["id"]: {
            "tags": deepcopy(unsorted_image["tags"]),
            "isGood": is_good,
            "opinion": [opinion]
        }
    }
    return img


def download_img(url: str) -> bytes:
    response = requests.get(url, headers=HEADERS)
    return response.content


@app.route('/', methods=['GET', 'POST'])
def index():
    unsorted_images = UnsortedImages()

    if request.method == 'POST':
        for unsorted_img in session["images_to_handle_on_be"]:
            is_good = request.form[str(unsorted_img["id"])] == "good"
            opinion = request.form[str(unsorted_img["id"])]
            img = prepare_sorted_img(unsorted_img, is_good, opinion)
            save_image(img)
            update_tags(list(img.values())[0]["tags"])
            delete_unsorted_image(unsorted_img)

        return redirect(url_for('index'))

    next_unsorted_images = unsorted_images.get_n_next(8)

    total_unsorted_images = unsorted_images.total
    session["images_to_handle_on_be"] = next_unsorted_images

    imgs = []
    for img in next_unsorted_images:
        img = {
            **img,
            "pageURL": URL.format(id=img["id"]),
            "img_content": None
        }

        if img["imgUrl"]:
            downloaded_img = download_img(img["imgUrl"])
            img_content = base64.b64encode(downloaded_img).decode('utf-8')
            img["img_content"] = img_content

        imgs.append(img)

    return render_template('index.html', imgs=imgs, total_unsorted_images=total_unsorted_images)


if __name__ == '__main__':
    app.run(debug=True)
