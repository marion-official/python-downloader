import sys

from python_downloader.python_downloader import download_domain

if __name__ == "__main__":
    argv: list[str] = sys.argv[1:]
    download_domain(argv)
