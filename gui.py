from copy import deepcopy
from pprint import pprint
import base64
from flask import Flask, render_template, request, session, redirect, url_for, abort
import requests

from configs import URL
from dao import UnsortedImages, delete_unsorted_image, save_image, update_tags
from ph_types import UnsortedImgType
from html_getter import HEADERS

app = Flask(__name__, template_folder='.')
app.secret_key = b'sjdhajhdkjahskdjhakjshdkajhsdkjahskjdh'


def prepare_sorted_img(unsorted_image: UnsortedImgType, is_good: bool) -> dict:
    img = {
        unsorted_image["id"]: {
            "tags": deepcopy(unsorted_image["tags"]),
            "isGood": is_good
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
        is_good = request.form["feedback"] == "good"
        feedback_img = session["next_unsorted_image"]
        img = prepare_sorted_img(feedback_img, is_good)
        save_image(img)
        update_tags(list(img.values())[0]["tags"])
        delete_unsorted_image(feedback_img)
        return redirect(url_for('index'))

    next_unsorted_image = unsorted_images.get_next(order_by="likelihood")

    if not next_unsorted_image:
        abort(404)

    session["next_unsorted_image"] = next_unsorted_image
    session["total_unsorted_images"] = unsorted_images.total
    session["img_url"] = URL.format(id=next_unsorted_image["id"])

    img_content = None
    is_video_content = None

    if next_unsorted_image["imgUrl"]:
        downloaded_img = download_img(next_unsorted_image["imgUrl"])
        img_content = base64.b64encode(downloaded_img).decode('utf-8')

    return render_template('index.html', img_content=img_content, is_video=is_video_content)


if __name__ == '__main__':
    app.run(debug=True)
