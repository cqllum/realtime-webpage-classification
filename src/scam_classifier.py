# src/scam_classifier.py
##########################################################################
# File: scam_classifier.py                                               #
# Description: Classifies websites as legitimate or potential scams.     #
# Author: cqllum                                                         #
# Date: 2024-10-23                                                       #
##########################################################################


import re
from urllib.parse import urlparse
import requests

def classify_legitimacy(url, content, keywords):
    """Classify the legitimacy of a website based on URL, content, and keywords."""
    legitimacy_factors = {
        "legitimate": [
            "contact", "support", "about us", "privacy policy", 
            "terms of service", "secure payment", "trusted"
        ],
        "scam": [
            "easy money", "guaranteed returns", "free trial", 
            "exclusive offer", "limited time", "urgent", "win", 
            "congratulations", "click here", "verify your account", 
            "100% guarantee"
        ],
    } # can be extended, but at the moment could cause false positives.. not taken for gospel!

    # 1. Check keywords for scam-related language
    scam_score = sum(1 for keyword in keywords if keyword in legitimacy_factors["scam"])
    legit_score = sum(1 for keyword in keywords if keyword in legitimacy_factors["legitimate"])
     
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    scam_style_domains = [".biz", ".xyz", ".info", ".top", ".club", ".loan"] # not an exhaustive list, POC for now too..
    if any(ext in domain for ext in scam_style_domains):
        scam_score += 1
    
    # 3. Check for HTTPS
    if not url.startswith('https://'):
        scam_score += 1

    # 4. Check for lack of contact information
    if not re.search(r"(contact|about|privacy)", content, re.IGNORECASE):
        scam_score += 1

    # 5. Decision making
    return "potential scam" if scam_score > legit_score else "legitimate"
