# src/processor.py
##########################################################################
# File: processor.py                                                     #
# Description: Contains functions for text preprocessing and keyword     #
#              extraction.                                               #
# Author: cqllum                                                         #
# Date: 2024-10-23                                                       #
##########################################################################


import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

# Ensure NLTK resources are downloaded
nltk.download('stopwords')

# Load stop words once to avoid repeated downloads
STOP_WORDS = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean and preprocess the input text."""
    # Convert HTML to plain text
    text = re.sub(r'<[^>]+>', ' ', text)  # Remove HTML tags
    text = re.sub(r'&[a-z]+;', ' ', text)  # Remove HTML entities (e.g. &amp;)
    
    # Lowercase and remove non-alphabetic characters
    text = re.sub(r'[^a-z\s]', '', text.lower())
    
    # Tokenize and remove stop words
    words = [word for word in text.split() if word not in STOP_WORDS]
    
    return ' '.join(words)

def extract_keywords(texts, top_n=10):
    """Extract important keywords from a list of texts using TF-IDF."""
    vectorizer = TfidfVectorizer(max_df=1.0, min_df=1, stop_words='english')
    
    # Fit and transform the texts to calculate the TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Get feature names (words) and sum up their TF-IDF scores
    feature_names = vectorizer.get_feature_names_out()
    summed_tfidf = tfidf_matrix.sum(axis=0)
    
    # Sort the words by importance and return the top_n keywords
    sorted_items = sorted(zip(summed_tfidf.A1, feature_names), reverse=True)
    return [word for _, word in sorted_items[:top_n]]

def generate_site_description(keywords, content):
    """Generate a site description based on keywords and content."""
    keywords_str = ', '.join(keywords)
    content_preview = content[:150]  # Preview the first 150 characters
    return f"This site is about {keywords_str}. The content mainly discusses: {content_preview}..."

