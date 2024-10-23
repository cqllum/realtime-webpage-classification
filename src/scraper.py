# src/scraper.py
##########################################################################
# File: scraper.py                                                       #
# Description: Scrapes website content, including title, meta tags, and  #
#              images.                                                   #
# Author: cqllum                                                         #
# Date: 2024-10-23                                                       #
##########################################################################


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import whois

def scrape_website(url):
    """Scrape website content, title, meta description, images, and internal links."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' # change to your preference
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape title
        title = soup.title.string if soup.title else 'No Title Found'

        # Scrape meta description
        meta_description = (
            soup.find('meta', attrs={'name': 'description'})['content']
            if soup.find('meta', attrs={'name': 'description'}) else 'No Description Found'
        )

        # Scrape images paths
        images = [img['src'] for img in soup.find_all('img', src=True)]

        # Scrape all internal links that are found on the web page
        internal_links = {urljoin(url, link['href']) for link in soup.find_all('a', href=True)}

        # Get WHOIS information
        domain_info = whois.whois(url)

        return {
            'success': True,
            'content': response.text,
            'title': title,
            'meta_description': meta_description,
            'images': images,
            'internal_links': list(internal_links),  # Convert set to list for JSON serialization
            'hostname': urlparse(url).hostname,
            'domain_info': domain_info
        }

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {
            'success': False,
            'hostname': None,
            'url': url,
            'error': str(e),
            'content': None,
            'internal_links': None
        }
