from bs4 import BeautifulSoup
import requests

import argparse
import os
import sys
from urllib.request import urlretrieve
from urllib.parse import urlparse, urljoin

from general_download.general_page_downloader import GeneralPageDownloader
from utils import get_basename_from_url


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
    home_page = GeneralPageDownloader(url)
    domain = home_page.get_domain()
    print(f"Working on the domain:  {domain}")

    # create dirs
    print("Creating directories")
    domain_dir = os.path.join(os.getcwd(), 'output', domain)
    css_dir = os.path.join(domain_dir, 'css')
    img_dir = os.path.join(domain_dir, 'img')

    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # download the HTML and parse it
    print("download the HTML")
    soup = home_page.download_html()

    # download files and change tags
    print("deal with IMGs")
    home_page.deal_with_tag_img()
    home_page.deal_with_tag_links()
    # home_page.deal_with_scripts()

    # write the HTML modified
    with open(f'output/{domain}/index.html', 'w') as index_file:
        index_file.write(soup.prettify())


if __name__ == "__main__":
    sys.exit(main())

