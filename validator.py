from copy import deepcopy
from dao import UnsortedImages, save_image, update_tags, delete_unsorted_image
from configs import URL
from pprint import pprint
from utils import get_img_id
from termcolor import colored


def parse_unsorted_image(unsorted_image: dict) -> tuple[str, bool, float]:
    url, is_good, likelihood = "", False, 0.0

    for key in unsorted_image.keys():
        match key:
            case "isGood":
                is_good = unsorted_image[key]
            case "likelihood":
                likelihood = unsorted_image[key]
            case _ :
                url = URL.format(id=key)

    return url, is_good, likelihood


def prepare_sorted_img(unsorted_image: dict, is_good: bool) -> dict:
    img_id = get_img_id(unsorted_image)
    img = {img_id: {}}
    for k, v in unsorted_image.items():
        if k == "isGood":
            img[img_id][k] = is_good
        elif k.isnumeric():
            img[img_id]["tags"] = deepcopy(v)
    return img


def main():
    unsorted_images = UnsortedImages()

    while True:
        print("-" * 50)
        if not (next_unsorted_image := unsorted_images.get_next()):
            print("No more unsorted images")
            break

        url, is_good, likelihood = parse_unsorted_image(next_unsorted_image)
        print(url)
        print(colored(is_good, "green" if is_good else "red"), likelihood)

        match input("Is it good? (y/n): ").lower():
            case "y":
                is_good = True
            case "n":
                is_good = False
            case _ :
                print("Invalid input")
                continue
        
        img = prepare_sorted_img(next_unsorted_image, is_good)
        save_image(img)
        tags = list(img.values())[0]["tags"]
        update_tags(tags)
        delete_unsorted_image(next_unsorted_image)


if __name__ == "__main__":
    main()
