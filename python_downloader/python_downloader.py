"""Main module."""
import requests
import argparse
import os
import sys
import urllib
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='The URL to download')
    args = parser.parse_args()

    url = args.url
    download_domain(url)


def download_domain(url):
    domain = get_domain_from_url(url)
    print(domain)
    if not os.path.exists(domain):
        os.mkdir(domain)
        os.mkdir(f'{domain}/css')
        os.mkdir(f'{domain}/img')
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    deal_with_tag_img(soup, domain)
    deal_with_tag_links(soup, domain)
    deal_with_scripts(soup)
    with open(f'{domain}/index.html', 'w') as index_file:
        index_file.write(soup.prettify())


def get_basename_from_url(url=None):
    if url is None:
        return None
    parsed_url = urlparse(url)
    url_path = parsed_url.path
    return os.path.basename(url_path)


def get_domain_from_url(url=None):
    if url is None:
        return None
    parsed_url = urlparse(url)
    return parsed_url.netloc


def deal_with_tag_links(soup, domain):
    """
    Dealing with link tags, for CSS only for now
    """
    links = soup.find_all('link')
    for link in links:
        # print(link.get('href'))
        # print(link.get('rel'))

        # if the link tag is a CSS file
        if "stylesheet" in link.get('rel'):
            # print("CSS")

            # take the name of the file
            base_name = get_basename_from_url(link.get('href'))

            # if there is no basename, next
            if base_name is None:
                continue

            # if the file already exists, next
            if os.path.isfile(f'{domain}/css/{base_name}'):
                continue

            # download the file
            with open(f'{domain}/css/{base_name}', 'w') as css_file:
                response = requests.get(link.get('href'))
                css_file.write(str(response.content))
                css_file.close()

            # update link tag to the new file
            link['href'] = f'./css/{base_name}'


def deal_with_tag_img(soup, domain):
    imgs = soup.find_all('img')
    for img in imgs:
        src = img.get('src')

        if src is None:
            continue

        # take the name of the file
        base_name = get_basename_from_url(src)

        # if there is no basename, next
        if base_name is None:
            continue

        # if the file is already present, next
        if os.path.isfile(f'{domain}/img/{base_name}'):
            continue
        print(src)
        # download the image
        urllib.request.urlretrieve(src, f'{domain}/img/{base_name}')

        # update the image with the new file
        img['src'] = f'./img/{base_name}'


def deal_with_scripts(soup):
    scripts = soup.find_all('script')
    for script in scripts:
        script.decompose()


if __name__ == "__main__":
    sys.exit(main())

