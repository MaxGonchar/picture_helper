import argparse

from data_repo.backup import do_backup, do_restore


def main() -> None:
    parser = argparse.ArgumentParser(description="Backup and restore data")
    parser.add_argument(
        "-d", "--do",
        action="store_true",
        help="Backup data to a zip file",
    )
    parser.add_argument(
        "-r", "--restore",
        action="store_true",
        help="Restore data from a zip file",
    )

    args = parser.parse_args()

    if args.do:
        do_backup()
    elif args.restore:
        do_restore()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
