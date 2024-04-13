"""Console script for python_downloader."""
import argparse
import sys


def main():
    """Console script for python_downloader."""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The URL to download')
    parser.add_argument('-a', '--all', help='Download all the website', action='store_true')

    #parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    if args.all:
        print('all is select')

    #print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "python_downloader.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
