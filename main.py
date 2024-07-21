from html_getter import get_html
from html_parser import parse_html
from data_handler import update_data


def main():
    while True:
        url = input("URL: ")
        is_good = ""

        while is_good not in ("y", "n"):
            is_good = input("Is it good (y/n): ")

        update_data(parse_html(get_html(url)), is_good == "y")
        print("Done")


if __name__ == "__main__":
    main()
