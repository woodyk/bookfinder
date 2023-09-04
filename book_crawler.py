#!/usr/bin/env python3
#
# getit.py

import os
import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            continue
        urls.add(href)
        if ".pdf" in href:
            download_pdf(href)
    return urls

def download_pdf(pdf_url):
    # Send a GET request to the PDF URL
    response = requests.get(pdf_url)

    # Get the PDF's name from its URL
    pdf_name = os.path.basename(pdf_url)

    # Write the PDF to a file
    with open(pdf_name, 'wb') as f:
        f.write(response.content)

    print(f'Downloaded: {pdf_name}')

def main(url):
    # Crawl all webpages of the website
    all_site_links = get_all_website_links(url)
    for link in all_site_links:
        get_all_website_links(link)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument('url', type=str, help='The website to crawl')
    args = parser.parse_args()
    main(args.url)

