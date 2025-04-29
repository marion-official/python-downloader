from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse, ParseResult


@dataclass
class URLInfo:
    """
    Dataclass dedicated to the single page URL to download

    url: str The original URL of the page
    downloaded: bool True if the URL has been downloaded
    local_base_dir: str The local directory where the URL will be downloaded
    local_name: str The local name of the URL being downloaded
    url_parsed: str The parsed URL from the url
    """
    url: str
    downloaded: bool = False
    local_base_dir: str = 'output'
    local_name: str | None = None
    url_parsed: ParseResult = None
    _local_url: str | None = None

    def set_as_downloaded(self, downloaded: bool = True):
        self.downloaded = downloaded

    def get_local_url(self, extension: str = 'html') -> str:
        """
        Find the name of the file by the url
        """
        if self._local_url:
            print("already written", self._local_url)
            return f"{self._local_url}.{extension}"

        self.url_parsed = urlparse(self.url)

        if not self.local_name:
            if self.url_parsed.path:
                path_split = self.url_parsed.path.split("/")
                self.local_name = path_split[-1]

            elif self.url_parsed.netloc:
                self.local_name = self.url_parsed.netloc
            else:
                raise NotImplementedError(
                    f"Still need to implement the case where url {self.url}: {urlparse(self.url)}")

        self._local_url = f'{self.local_base_dir}/{self.url_parsed.netloc}/{self.local_name}'
        return f"{self._local_url}.{extension}"
