from bs4 import BeautifulSoup
import requests

import argparse
import os
import sys
from urllib.request import urlretrieve
from urllib.parse import urlparse, urljoin


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The URL to download')
    args = parser.parse_args()

    url = args.url
    download_domain(url)


def download_domain(url):
    """
    Download HTML, CSS, and images from a website and update links.
    """
    domain = get_domain_from_url(url)
    print(domain)

    # create dir
    domain_dir = os.path.join(os.getcwd(), domain)
    css_dir = os.path.join(domain_dir, 'css')
    img_dir = os.path.join(domain_dir, 'img')

    os.makedirs(css_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)

    # download the HTML and parse it
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # download files and change tags
    deal_with_tag_img(soup, domain)
    deal_with_tag_links(soup, domain)
    deal_with_scripts(soup)

    # write the HTML modified
    with open(f'{domain}/index.html', 'w') as index_file:
        index_file.write(soup.prettify())


def get_basename_from_url(url):
    """
    Get the base name (file name) from a URL.
    """
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    return os.path.basename(url_path)


def get_domain_from_url(url):
    """
    Get the domain (netloc) from a URL.
    """
    parsed_url = urlparse(url)
    return parsed_url.netloc


def deal_with_tag_links(soup, domain):
    """
    Process link tags (for CSS)
    """
    links = soup.find_all('link', rel='stylesheet')
    for link in links:
        href = link.get('href')

        if href:
            # take the name of the file
            base_name = get_basename_from_url(href)

            # if there is no basename, next
            if base_name:
                if href.startswith('/'):
                    href = urljoin(f'https://{domain}', href)

                # if the file is not already exists, download it
                if os.path.isfile(f'{domain}/css/{base_name}'):
                    response = requests.get(href)
                    with open(f'{domain}/css/{base_name}', 'wb') as css_file:
                        css_file.write(response.content)

                # update link tag to the new file
                link['href'] = f'./css/{base_name}'


def deal_with_tag_img(soup, domain):
    """
    Process img tags (for images).
    """
    imgs = soup.find_all('img')
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
                    src = urljoin(f'https://{domain}', src)

                # if the file not already present, download it
                if not os.path.isfile(f'{domain}/img/{base_name}'):
                    urlretrieve(src, f'{domain}/img/{base_name}')

                # update the image with the new file
                img['src'] = f'./img/{base_name}'


def deal_with_scripts(soup):
    """
    Remove script tags from the HTML.
    """
    scripts = soup.find_all('script')
    for script in scripts:
        script.decompose()


if __name__ == "__main__":
    sys.exit(main())
