from __future__ import annotations

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests
import os

from python_downloader.utils import get_basename_from_url, sanitize_url, download_file, URLInfo


class GeneralPageDownloader:
    """
    This class is dedicated to download a generic, single page
    """
    def __init__(self, url_info: URLInfo) -> None:
        self.__url_info: URLInfo = url_info
        self.__url: str = url_info.url
        self.__url_parsed = urlparse(self.__url)
        self.__html_response = None
        self.__soap = None
        self.__domain: str | None = None
        self.__scheme: str | None = None
        self.parse_url()

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
        self.__soap = BeautifulSoup(self.__html_response.content, 'html.parser')
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

            print(f"Downloading {src}")

            # Take the name of the file
            base_name = get_basename_from_url(src)

            # If there is no basename, next
            if not base_name:
                continue

            # If the src is relative make it absolute
            if src.startswith('/'):
                src = urljoin(f'{self.__scheme}://{self.__domain}', src)
                print(f"It was an relative url, modified to {src}")

            # Sanitize the URL
            src = sanitize_url(src)

            file_name = download_file(src, base_name, self.__domain, "img")

            # update the image with the new file
            img['src'] = f'./img/{file_name}'

    def deal_with_tag_links(self):
        """
        Process link tags (for CSS)
        """
        links = self.__soap.find_all('link', rel='stylesheet')
        for link in links:
            href = link.get('href')

            if href:
                # take the name of the file
                base_name = get_basename_from_url(href)

                # if there is no basename, next
                if base_name:
                    if href.startswith('/'):
                        href = urljoin(f'https://{self.__domain}', href)

                    # if the file is not already exists, download it
                    if os.path.isfile(f'output/{self.__domain}/css/{base_name}'):
                        response = requests.get(href)
                        with open(f'output/{self.__domain}/css/{base_name}', 'wb') as css_file:
                            css_file.write(response.content)

                    # update link tag to the new file
                    link['href'] = f'./css/{base_name}'

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

            # if there is no link, skip it
            if not href or href == "#":
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

        file_name = f'output/{self.__domain}/page.html'

        # if we have already a local address, use it
        if self.__url_info.local_url:
            file_name = self.__url_info.local_url
        else:
            # else find one
            file_name = self.__url_info.get_local_url()

        with open(file_name, 'w') as index_file:
            index_file.write(self.__soap.prettify())
