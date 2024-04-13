import os
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin

from utils import get_basename_from_url


class GeneralPageDownloader:
    """
    This class is for downloading a generic page
    """

    def __init__(self, url: str) -> None:
        self.__url: str = url
        self.__url_parsed = urlparse(url)
        self.__domain: str | None = None
        self.__html_response = None
        self.__soap = None
        self.parse_url()

    def parse_url(self) -> None:
        """
        Support method to parse the URL and extract domain information.

        This method is intended for internal use within the class.
        """
        self.__domain = self.__url_parsed.netloc

    def get_domain(self) -> str:
        return self.__domain

    def download_html(self) -> BeautifulSoup:
        """
        This method is to download the html and process it
        """
        self.__html_response = requests.get(self.__url)
        self.__soap = BeautifulSoup(self.__html_response.content, 'html.parser')
        return self.__soap

    def deal_with_tag_img(self) -> None:
        """
        Process img tags (for images).
        """
        imgs = self.__soap.find_all('img')
        for img in imgs:
            src = img.get('src')

            # make sure we have a src
            if src:
                # take the name of the file
                base_name = get_basename_from_url(src)

                # if there is no basename, next
                if base_name:
                    # if the src is relative make it absolute
                    if src.startswith('/'):
                        src = urljoin(f'https://{self.__domain}', src)

                    # if the file not already present, download it
                    if not os.path.isfile(f'output/{self.__domain}/img/{base_name}'):
                        urlretrieve(src, f'output/{self.__domain}/img/{base_name}')

                    # update the image with the new file
                    img['src'] = f'./img/{base_name}'

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
