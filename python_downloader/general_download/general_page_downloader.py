from __future__ import annotations

import logging
from urllib.error import HTTPError
from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup

from python_downloader.urlinfo import URLInfo
from python_downloader.utils import get_basename_from_url, sanitize_url, download_file, is_valid_url, \
    get_random_user_agents

logger = logging.getLogger(__name__)


class GeneralPageDownloader:
    """
    This class is dedicated to download a generic, single page
    """

    def __init__(self, url_info: URLInfo) -> None:
        self.url_info: URLInfo = url_info
        self.__url: str = url_info.url
        self.__url_parsed = urlparse(self.__url)
        self.__html_response = None
        self.__soap = None
        self.__domain: str | None = None
        self.__scheme: str | None = None
        self.user_agent: str | None = None
        self.parse_url()
        self.set_user_agents()

    def get_soap(self):
        return self.__soap

    def set_user_agents(self):
        if not self.user_agent:
            self.user_agent = get_random_user_agents()
            logger.debug(f"User agent: {self.user_agent}")

    def parse_url(self) -> None:
        """
        Support method to parse the URL and extract domain information.

        This method is intended for internal use within the class.
        """
        self.__domain = self.__url_parsed.netloc
        self.__scheme = self.__url_parsed.scheme

    def get_domain(self) -> str:
        return self.__domain

    def download_html(self) -> BeautifulSoup:
        """
        This method is to download the html and process it
        """
        self.__html_response = requests.get(self.__url_parsed.geturl())
        self.__soap = BeautifulSoup(self.__html_response.content, 'html.parser', from_encoding='utf-8')
        return self.__soap

    def deal_with_tag_img(self) -> None:
        """
        Process img tags (for images).
        """
        imgs = self.__soap.find_all('img')
        for img in imgs:
            src = img.get('src')

            # If the image has no src attribute, just ignore it
            if not src:
                continue

            logger.info(f"Downloading IMG {src}")

            # Take the name of the file
            base_name = get_basename_from_url(src)

            # If there is no basename, next
            if not base_name:
                logger.error(f"no baasename for {src}")
                continue

            # If the src is relative make it absolute
            if src.startswith('/'):
                src = urljoin(f'{self.__scheme}://{self.__domain}', src)
                logger.debug(f"It was an relative url, modified to {src}")

            # Sanitize the URL
            src = sanitize_url(src)

            logger.debug(f"Downloading img file: {src}")

            try:
                file_name = download_file(src, base_name, self.__domain, "img", user_agent=self.user_agent)
            except HTTPError as e:
                logger.error(f"Error downloading {src} {e}")
                continue

            # update the image with the new file
            img['src'] = f'./img/{file_name}'

    def deal_with_tag_links(self):
        """
        Process link tags (for CSS)
        """
        links = self.__soap.find_all('link', rel='stylesheet')
        for link in links:
            href = link.get('href')

            if not href:
                continue

            base_name = get_basename_from_url(href)

            if not base_name:
                logger.error(f"no baasename for {href}")
                continue

            if href.startswith('/'):
                href = urljoin(f'https://{self.__domain}', href)

            href = sanitize_url(href)

            logger.info(f"Downloading CSS {href}")

            try:
                file_name = download_file(href, base_name, self.__domain, "css", user_agent=self.user_agent)
            except HTTPError as e:
                logger.error(f"Error downloading {href} {e}")
                continue

            # update link tag to the new file
            link['href'] = f'./css/{file_name}'

    def deal_with_scripts(self):
        """
        Remove script tags from the HTML.
        """
        scripts = self.__soap.find_all('script')
        for script in scripts:
            script.decompose()

    def get_links_in_domain(self) -> dict[str, URLInfo]:
        """
        obtain the list of links in the page pointing to in the same domain
        """
        results: dict[str, URLInfo] = {}

        links = self.__soap.find_all('a')
        for link in links:
            href = link.get('href')

            if not is_valid_url(href):
                logger.debug(f"Invalid page href: {href}")
                continue
            # if there is no link, skip it
            if not href:
                logger.debug("Href not found")
                continue

            # If the src is relative make it absolute
            if href.startswith("/"):
                href = urljoin(f'{self.__scheme}://{self.__domain}', href)

            if href not in results:
                results[href] = URLInfo(href)

        return results

    def write_html(self) -> None:
        """
        Write the html page on disk
        """

        file_name = self.url_info.get_local_url()

        with open(file_name, 'w') as index_file:
            index_file.write(self.__soap.prettify())
