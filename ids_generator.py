import argparse

from data_repo.id import Id
from domain import Domain

def main() -> None:
    parser = argparse.ArgumentParser(description="Generate integer ids in provided range")
    parser.add_argument(
        "--start", "-s",
        type=int,
        help="Start of the range",
    )
    parser.add_argument(
        "--end", "-e",
        type=int,
        help="End of the range",
    )
    args = parser.parse_args()
    start = args.start
    end = args.end

    # check that start is less than end
    if start >= end:
        raise ValueError("Start must be less than end")
    
    if input(f"Do you want to generate ids from {start} to {end}? [y/n]: ") != "y":
        return
    
    print(f"Generating ids from {start} to {end}")
    Id(Domain()).add_ids(map(str, range(start, end + 1)))
    print("Ids generated successfully")


if __name__ == "__main__":
    main()
