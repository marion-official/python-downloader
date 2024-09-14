from __future__ import annotations

import argparse
import sys

from urllib.parse import urlparse

from general_download import GeneralDomainDownloader

# TODO set this in a conf file
configs = {
    "depth_of_pages_to_download":  2
}

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The URL to download')
    args = parser.parse_args()

    url: str = args.url
    print(f"Downloading: {url}")
    download_domain(url)


def download_domain(url: str) -> None:
    """
    Download HTML, CSS, and images from a website and update links.
    """
    url_parsed = urlparse(url)
    home_page = GeneralDomainDownloader(url_parsed, configs)
    print(f"Working on the domain:  {url_parsed.netloc}")

    # create dirs
    home_page.create_dir()

    # download content
    home_page.download_content()


if __name__ == "__main__":
    sys.exit(main())

