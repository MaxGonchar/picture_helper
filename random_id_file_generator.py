from random import shuffle
from os.path import join

from configs import SHUFFLED_ID_FILE, DATA_FOLDER


def generate_range(start: int, end: int) -> list[int]:
    return list(range(start, end + 1))


def shuffle_list(list_: list[int]) -> list[int]:
    shuffle(list_)
    return list_


def main(start: int, end: int) -> None:
    shuffled_list = shuffle_list(generate_range(start, end))
    with open(join(DATA_FOLDER, SHUFFLED_ID_FILE), "w") as f:
        f.write(str(shuffled_list))


if __name__ == "__main__":
    main(25021, 1000000)
