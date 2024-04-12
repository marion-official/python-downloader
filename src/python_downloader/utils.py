import os
from urllib.parse import urlparse


def get_basename_from_url(url):
    """
    Get the base name (file name) from a URL.
    """
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    return os.path.basename(url_path)
