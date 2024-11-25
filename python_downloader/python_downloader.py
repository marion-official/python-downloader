from __future__ import annotations

import argparse
from urllib.parse import urlparse

from python_downloader.general_download import GeneralDomainDownloader

configs = {
    "depth_of_pages_to_download":  2
}

def download_domain(argv: list[str]) -> None:
    """
    Download HTML, CSS, and images from a website and update links.
    """
    parser = argparse.ArgumentParser(description="""A tool to help you download an entire website,
        or part of it, and organize the downloaded content (images, HTML, videos, CSS, etc.)
        into separate directories.
        """)
    parser.add_argument("url")
    parser.add_argument("-d", "--depth", default=2, type=int)
    arguments = parser.parse_args(argv)

    configs['depth_of_pages_to_download'] = arguments.depth
    url:  str = arguments.url
    url_parsed = urlparse(url)

    home_page = GeneralDomainDownloader(url_parsed, configs)
    print(f"Working on the domain:  {url_parsed.netloc}")

    home_page.create_dir()

    home_page.download_content()

