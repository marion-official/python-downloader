from __future__ import annotations

import os
from dataclasses import dataclass
import re
import requests
import logging
from urllib.parse import urlparse, urlunparse, quote
from urllib.request import urlretrieve
from hashlib import md5
from random import choice

from click import FileError

from python_downloader.file import FileName
from python_downloader.config import USER_AGENTS_LIST_LOCATION, HTTP_RESPONSE_ACCEPTED

logger = logging.getLogger(__name__)


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
    sanitized_url = urlunparse((scheme, netloc, path, params, query, fragments))

    return str(sanitized_url)


def download_file(src: str, base_name: str, domain: str, directory: str, md5_remote: str = "",
                  user_agent: str = "") -> str:
    """
    Download the file handling duplicates
    """
    # if the file not already present, download it
    filename_local: str = f'output/{domain}/{directory}/{base_name}'
    if not os.path.isfile(filename_local):
        headers = {
            "User-Agent": user_agent
        }
        logger.debug(f"retrieve({src}, {filename_local}")
        response = requests.get(src, headers=headers)
        if response.status_code in HTTP_RESPONSE_ACCEPTED:
            try:
                with open(filename_local, "wb") as f:
                    f.write(response.content)
            except OSError as e:
                logger.debug(f"Exception while writing {filename_local}: {e}")
                raise
        else:
            logger.error(f"{src} returned {response.status_code}")
        # urlretrieve(src, filename_local)
    else:
        # If the file is already present
        file = FileName(base_name)

        # get remote MD5 checksum from parameter or calculate it
        _md5_remote: str = md5_remote if md5_remote else get_md5_from_url(src)

        # get the current file MD5
        md5_file: str = get_md5(filename_local)
        if md5_file == _md5_remote:
            return base_name
        else:
            file.increase_version()
            return download_file(src=src, base_name=file.get_filename(), domain=domain, directory=directory,
                                 md5_remote=_md5_remote)

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


def is_valid_url(url):
    """
    Check if a url is valid
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


@dataclass
class URLInfo:
    """
    Dataclass dedicated to the single page URL to download
    """
    url: str
    downloaded: bool = False
    local_url: None | str = None

    def set_as_downloaded(self, downloaded: bool = True):
        self.downloaded = downloaded

    def get_local_url(self) -> str:
        """
        Find the name of the file by the url
        """
        if self.local_url:
            return self.local_url

        scheme, netloc, path, params, query, fragments = urlparse(self.url)

        base_name = None
        if path:
            path_split = path.split("/")
            base_name = path_split[-1]

        elif netloc:
            base_name = netloc
        else:
            raise NotImplementedError(f"Still need to implement the case where url {self.url}: {urlparse(self.url)}")

        return f'output/{netloc}/{base_name}.html'


def get_random_user_agents() -> str:
    """
    Returns a random user-agent from our list
    """
    try:
        with open(USER_AGENTS_LIST_LOCATION, 'r') as file:
            content = file.readlines()
            user_agent = choice(content)
            return user_agent.strip()
    except FileNotFoundError as e:
        logger.error(f"List file of user-agents not found in {USER_AGENTS_LIST_LOCATION}: {e}")
        raise
