from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse, ParseResult


@dataclass
class URLInfo:
    """
    Dataclass dedicated to the single page URL to download

    url: str The original URL of the page
    downloaded: bool True if the URL has been downloaded
    local_url: str The local URL on disk for the page
    url_parsed: str The parsed URL from the url
    """
    url: str
    downloaded: bool = False
    local_url: None|str = None
    url_parsed: ParseResult = None

    def set_as_downloaded(self, downloaded: bool = True):
        self.downloaded = downloaded

    def get_local_url(self) -> str:
        """
        Find the name of the file by the url
        """
        if self.local_url:
            print("already written", self.local_url)
            return self.local_url

        self.url_parsed = urlparse(self.url)

        base_name = None
        if self.url_parsed.path:
            path_split = self.url_parsed.path.split("/")
            base_name = path_split[-1]

        elif self.url_parsed.netloc:
            base_name = self.url_parsed.netloc
        else:
            raise NotImplementedError(f"Still need to implement the case where url {self.url}: {urlparse(self.url)}")

        return f'output/{self.url_parsed.netloc}/{base_name}.html'
