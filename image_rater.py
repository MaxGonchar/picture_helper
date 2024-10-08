from configs import URL
from html_getter import get_html
from html_parser import parse_html
from predictor import predict_likelihood_of_image
import dao
from img_data_transformer import prepare_unsorted_img
from time import sleep
from termcolor import colored
from data_repo.id import NextShuffledImgID, Domain

SLEEP_TIME = 1


def rate_image():
    with NextShuffledImgID(Domain()) as img_id:

        if not img_id:
            print("No more image ids to rate")
            return

        url = URL.format(id=img_id)

        if html := get_html(url):
            img_data = parse_html(html)
            is_good, likelihood = predict_likelihood_of_image(img_data["tags"])
            print(img_data["id"], colored(is_good, "green" if is_good else "red"), likelihood)
            dao.save_unsorted_image(prepare_unsorted_img(img_data, is_good, likelihood))


def main(number: int) -> None:
    for i in range(number):
        print(i + 1, end=" ")
        rate_image()
        sleep(SLEEP_TIME)


if __name__ == "__main__":
    main(1000)
