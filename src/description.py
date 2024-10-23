# src/description.py

def generate_site_description(keywords, content):
    """Generate a description for the website based on keywords and content."""
    
    description = create_basic_description(keywords)
    description += add_detail_based_on_content(content)
    
    return description

def create_basic_description(keywords):
    """Create a basic description using the most frequent keywords."""
    keyword_list = keywords[:5]  # Get the top 5 keywords
    return f"This website discusses topics such as {', '.join(keyword_list)} and more."

def add_detail_based_on_content(content):
    """Add detail to the description based on the content length."""
    if len(content.split()) > 1000: # this can be changed, just a POC..
        return " It contains comprehensive content and covers in-depth topics."
    return " It provides concise information on these subjects."
