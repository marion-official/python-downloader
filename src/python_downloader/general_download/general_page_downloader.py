from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urljoin


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


