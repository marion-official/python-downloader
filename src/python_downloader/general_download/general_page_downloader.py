from urllib.parse import urlparse, urljoin


class GeneralPageDownloader:
    """
    This class is for downloading a generic page
    """

    def __init__(self, url: str) -> None:
        self.__url: str = url
        self.__url_parsed = urlparse(url)
        self.__domain: str | None = None
        self.parse_url()

    def parse_url(self) -> None:
        """
        Support method to parse the URL and extract domain information.

        This method is intended for internal use within the class.
        """
        self.__domain = self.__url_parsed.netloc

    def get_domain(self) -> str:
        return self.__domain

