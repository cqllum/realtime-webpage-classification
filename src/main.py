# src/main.py
##########################################################################
# File: main.py                                                          #
# Description: Main processing logic for website classification.         #
# Author: cqllum                                                         #
# Date: 2024-10-23                                                       #
##########################################################################

from src.scraper import scrape_website
from src.processor import preprocess_text, extract_keywords, generate_site_description
from src.classifier import classify_website
from src.scam_classifier import classify_legitimacy

def process_website_data(url):
    """Process the website data by scraping and analyzing its content."""
    # Step 1: Scrape the website
    website_data = scrape_website(url)
    
    if not website_data.get('success', False):
        return website_data  # Return the error message if scraping failed

    # Extract relevant data only if the scrape was successful
    content = website_data.get('content')
    
    if content is None:
        return {
            'success': False,
            'url': url,
            'hostname': website_data['hostname'],
            'error': 'No content retrieved from the website.'
        }

    # Step 2: Preprocess the content
    clean_content = preprocess_text(content)

    # Step 3: Extract keywords
    keywords = extract_keywords([clean_content], top_n=10)

    # Step 4: Classify the website
    category = classify_website(keywords)

    # Step 5: Generate a site description
    description = generate_site_description(keywords, clean_content)

    # Step 6: Classify site legitimacy (legitimate or scam)
    legitimacy = classify_legitimacy(url, clean_content, keywords)

    # Gather all data to return
    return compile_results(url, website_data, keywords, category, description, legitimacy)

def compile_results(url, website_data, keywords, category, description, legitimacy):
    """Compile and return the final result."""
    return {
        'success': True,
        'url': url,
        'hostname': website_data['hostname'],
        'title': website_data['title'],
        'meta_description': website_data['meta_description'],
        'images': website_data['images'],
        'internal_links': website_data['internal_links'],
        'domain_info': str(website_data['domain_info']),  # Convert WHOIS info to string
        'keywords': keywords,
        'category': category,
        'description': description,
        'legitimacy': legitimacy,
    }

def main(url):
    """Main function to process the given URL."""
    return process_website_data(url)

if __name__ == "__main__": 
    pass
