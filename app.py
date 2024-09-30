import sys

from python_downloader.python_downloader import download_domain

if __name__ == "__main__":
    url: str = sys.argv[1]
    download_domain(url)
