from __future__ import annotations

import os
from dataclasses import dataclass

from urllib.parse import urlparse,urlunparse, quote
from urllib.request import urlretrieve
from hashlib import md5

import re
import requests

from file import FileName


def get_basename_from_url(url: str) -> str:
    """
    Get the base name (file name) from a URL.
    """
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    return os.path.basename(url_path)


def sanitize_url(url: str) -> str:
    """
    Sanitize a URL percent-encoding any special characters
    """
    # Parse the URL
    scheme, netloc, path, params, query, fragments = urlparse(url)

    # Quote the path and query
    path = quote(path)
    query = quote(query, safe='=&')

    # Reconstruct the URL
    sanitized_url = urlunparse((scheme, netloc, path, params,query , fragments))

    return str(sanitized_url)


def download_file(src: str, base_name: str, domain: str, directory: str, md5_remote: str = "") -> str:
    """
    Download the file handling duplicates
    """
    # if the file not already present, download it
    if not os.path.isfile(f'output/{domain}/{directory}/{base_name}'):
        urlretrieve(src, f'output/{domain}/{directory}/{base_name}')
    else:
        # If the file is already present
        file = FileName(base_name)

        # get remote MD5 checksum from parameter or calculate it
        _md5_remote: str = md5_remote if md5_remote else get_md5_from_url(src)
        print(_md5_remote)

        # get the current file MD5
        md5_file: str = get_md5(f'output/{domain}/{directory}/{base_name}')
        print(md5_file)
        if md5_file == _md5_remote:
            return base_name
        else:
            file.increase_version()
            return download_file(src=src, base_name=file.get_filename(), domain=domain, directory=directory, md5_remote=_md5_remote)

    return base_name


def get_md5(file_path):
    """
    Compute the MD5 checksum of a file
    """
    hash_md5 = md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_md5_from_url(url: str) -> str:
    """
    Compute the MD5 checksum from a URL
    """
    response = requests.get(url, stream=True)
    hash_md5 = md5()
    for chunk in response.iter_content(chunk_size=4096):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def find_version_from_file(file_name: str) -> int:
    """
    Find the version number in the format `name_nn.ext` from a file name
    """
    # Split the file name in extension and base name
    base, _ = os.path.splitext(file_name)

    # Search if the base name end with a _nn number
    match = re.match(r'.*_(\d+)', base)
    if match:
        # if we have one, return the number as the counter
        return int(match.group(1))
    # if we don't have one, start from 0
    return 0

@dataclass
class URLInfo:
    """
    Dataclass dedicated to the single page URL to download
    """
    url: str
    downloaded: bool = False
    local_url: None|str = None

    def set_as_downloaded(self, downloaded: bool = True):
        self.downloaded = downloaded


    def get_local_url(self) -> str:
        """
        Find the name of the file by the url
        """
        # if we have already the url, use it
        if self.local_url:
            return self.local_url

        # Parse the URL
        scheme, netloc, path, params, query, fragments = urlparse(self.url)

        if path:
            path_split = path.split("/")
            return  f'output/{netloc}/{path_split[-1]}.html'

        raise NotImplementedError(f"Still need to implement the case where {urlparse(self.url)}")

        return f'output/{netloc}/page.html'
