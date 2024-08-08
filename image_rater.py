from configs import URL
from html_getter import get_html
from html_parser import parse_html
from predictor import predict_likelihood_of_image
import dao
from img_data_transformer import prepare_unsorted_img
from time import sleep

SLEEP_TIME = 1


def rate_image():
    with dao.NextImgID() as img_id:
        url = URL.format(id=img_id)

        if html := get_html(url):
            img_data = parse_html(html)
            is_good, likelihood = predict_likelihood_of_image(img_data)
            dao.save_unsorted_image(prepare_unsorted_img(img_data, is_good, likelihood))


if __name__ == "__main__":
    for _ in range(900):
        rate_image()
        sleep(SLEEP_TIME)
