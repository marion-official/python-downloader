import os

from urllib.parse import urlparse,urlunparse, quote


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

    return sanitized_url
