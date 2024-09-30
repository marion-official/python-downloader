from __future__ import annotations

import argparse
import sys
from urllib.parse import urlparse

from python_downloader.general_download import GeneralDomainDownloader

# TODO set this in a conf file
configs = {
    "depth_of_pages_to_download":  2
}

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

