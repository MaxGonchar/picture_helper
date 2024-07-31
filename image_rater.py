from os.path import join

from configs import DATA_FOLDER, ID_FILE, URL
from html_getter import get_html
from html_parser import parse_html
from predictor import predict_liklihood_of_image
import dao

# get last id from datastore
with open(join(DATA_FOLDER, ID_FILE), "r") as f:
    last_id = int(f.read())

# build url
url = URL.format(id=last_id)

# get image from url
if html := get_html(url):
    img_data = parse_html(html)
    liklihood = predict_liklihood_of_image(img_data)
    dao.save_unsorted_image(img_data, liklihood)

# update id in datastore
with open(join(DATA_FOLDER, ID_FILE), "w") as f:
    f.write(str(last_id + 1))
