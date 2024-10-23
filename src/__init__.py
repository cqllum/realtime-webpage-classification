# src/__init__.py

# Import the Scraper class if defined in scraper.py
from .scraper import scrape_website

# Import functions from processor.py
from .processor import preprocess_text, extract_keywords, generate_site_description

# Import functions from classifier.py
from .classifier import classify_website

# Import functions from scam_classifier.py
from .scam_classifier import classify_legitimacy

# Import the main function for processing a domain from main.py
from .main import main

# Optionally import anything else you might need
