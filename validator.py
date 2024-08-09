from copy import deepcopy
from dao import UnsortedImages, save_image, update_tags, delete_unsorted_image
from configs import URL
from termcolor import colored
from ph_types import UnsortedImgType


def parse_unsorted_image(unsorted_image: UnsortedImgType) -> tuple[str, bool, float]:
    return (
        URL.format(id=unsorted_image["id"]),
        unsorted_image["isGood"],
        unsorted_image["likelihood"]
    )


def prepare_sorted_img(unsorted_image: UnsortedImgType, is_good: bool) -> dict:
    img = {
        unsorted_image["id"]: {
            "tags": deepcopy(unsorted_image["tags"]),
            "isGood": is_good
        }
    }
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
