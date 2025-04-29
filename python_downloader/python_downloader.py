from __future__ import annotations

import argparse
import logging
from urllib.parse import urlparse, ParseResult

from python_downloader.general_download import GeneralDomainDownloader
from python_downloader.stackoverflow import StackoverflowDomainDownloader

logger = logging.getLogger(__name__)

known_domains: dict[str: any] = {
    "stackoverflow.com": StackoverflowDomainDownloader
}


class PythonDownloader:
    """
    This class represent the main application
    """

    def __init__(self, argv: list[str]):
        # the argv parameter given as input
        self.argv: list[str] = argv
        # the arguments parsed by argparse
        self.arguments: argparse.Namespace | None = None
        # the settings of the applications
        self.configs: dict[str, str | int] = {
            'depth_of_pages_to_download': 2
        }
        # the initial URL passed as input
        self.url: str | None = None
        # the url parsed in all it's components
        self.url_parsed: ParseResult | None = None

    def run(self):
        self.parse_arguments()
        self.set_variables()
        self.download_domain()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="""A tool to help you download an entire website,
                or part of it, and organize the downloaded content (images, HTML, videos, CSS, etc.)
                into separate directories.
                """)
        parser.add_argument("url")
        parser.add_argument("-d", "--depth", default=2, type=int, help="Depth of how many pages to download")
        parser.add_argument("-g", "--general", action='store_true', help="Force the domain to be treated as generic")

        self.arguments = parser.parse_args(self.argv)

    def set_variables(self):
        self.configs['depth_of_pages_to_download'] = self.arguments.depth
        self.url: str = self.arguments.url
        self.url_parsed = urlparse(self.url)

    def download_domain(self):
        logger.info(f"Working on the domain:  {self.url_parsed.netloc}")

        if self.url_parsed.netloc in known_domains and not self.arguments.general:
            logger.debug(f"Recognised domain {self.url_parsed.netloc}")
            page = known_domains[self.url_parsed.netloc](self.url_parsed, self.configs)
        else:
            logger.debug("Using general domain downloader")
            page = GeneralDomainDownloader(self.url_parsed, self.configs)

        page.create_dir()

        page.download_content()
