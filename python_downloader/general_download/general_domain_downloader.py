from __future__ import annotations

import os
import logging

from .general_page_downloader import GeneralPageDownloader
from python_downloader.utils import URLInfo

logger = logging.getLogger(__name__)


class GeneralDomainDownloader:
    """
    This class is for downloading a generic page
    """

    def __init__(self, url_parsed, configs: dict[str, int]) -> None:
        self.__url_parsed = url_parsed
        self.__config = configs
        self.__dept: int = 0
        self.hyperlinks_in_domain: dict[str, URLInfo] = {}

        self.init_hyperlinks_in_domain()

    def init_hyperlinks_in_domain(self):
        """
        Initialise the list of links to download with the index
        """
        self.hyperlinks_in_domain[self.__url_parsed.geturl()] = (
            URLInfo(self.__url_parsed.geturl(),
                    local_url=f'output/{self.__url_parsed.netloc}/index.html'))

    def download_content(self):
        """
        Download the content of the domain
        """
        while True:

            links_not_downloaded = {key: value for (key, value) in self.hyperlinks_in_domain.items() if
                                    not value.downloaded}

            # if there are no links to download, we have finished
            if not links_not_downloaded:
                logger.debug("No more links to download")
                break

            for page_to_download_url, page_to_download_file in links_not_downloaded.items():
                logger.debug(f"Downloading page: {page_to_download_url}")
                page = GeneralPageDownloader(page_to_download_file)

                # download the HTML and parse it
                logger.debug("download the HTML")
                page.download_html()

                # download images and change tags
                logger.debug("Deal with IMGs")
                page.deal_with_tag_img()

                # download CSS and change tags
                logger.debug("Deal with tag links")
                page.deal_with_tag_links()

                # download javascript and change tags
                logger.debug("Deal with scripts")
                page.deal_with_scripts()

                # deal with the hyperlinks to the same domain
                logger.debug("Deal with the hyperlinks to the same domain")
                self.hyperlinks_in_domain.update(page.get_links_in_domain())

                logger.debug("Print the page")
                page.write_html()

                # set this page as downloaded
                self.hyperlinks_in_domain[page_to_download_url].set_as_downloaded()

            # increase depth of 1
            self.__dept += 1

            # if we reached the depth threshold, stop
            if self.__dept >= self.__config['depth_of_pages_to_download']:
                logger.debug("Desired depth reached")
                break

    def create_dir(self):
        logger.debug("Creating directories")
        domain_dir = os.path.join(os.getcwd(), 'output', self.__url_parsed.netloc)
        css_dir = os.path.join(domain_dir, 'css')
        img_dir = os.path.join(domain_dir, 'img')

        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(img_dir, exist_ok=True)
