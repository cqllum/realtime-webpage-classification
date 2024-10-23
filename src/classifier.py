# src/classifier.py
######################################################################## #
# File: main.py                                                         #
# Description: Main processing logic for website classification.        #
# Author: Your Name                                                     #
# Date: YYYY-MM-DD                                                      #
#########################################################################


def classify_website(keywords):
    """Classifys a websites category based on the keywords found on the site."""
    categories = get_categories()
    
    # Compare keywords with category keywords
    for category, category_keywords in categories.items():
        if any(keyword in category_keywords for keyword in keywords):
            return category
    return "uncategorized"

def get_categories():
    """Prepares a list of categories."""
    return {
        "technology": [
            "software", "security", "development", "computer", "technology", "ai", 
            "cloud", "data", "machine learning", "programming", "blockchain", 
            "internet of things", "iot", "big data", "cybersecurity", "robotics", 
            "devops", "agile", "virtual reality", "augmented reality", "database", 
            "startup", "gadget", "tech news", "digital transformation", "innovation", 
            "mobile apps", "software engineering", "data science", "analytics"
        ],
        "health": [
            "medicine", "health", "fitness", "wellness", "doctor", "hospital", 
            "nutrition", "therapy", "mental health", "physical therapy", 
            "healthcare", "disease", "vaccine", "clinical trials", "preventive care", 
            "meditation", "yoga", "healthy living", "chronic illness", 
            "public health", "health insurance", "health technology", "nutritionist"
        ],
        "finance": [
            "stocks", "finance", "investment", "market", "trading", "economy", 
            "banking", "cryptocurrency", "savings", "loans", "mortgage", 
            "retirement", "wealth management", "financial planning", "real estate", 
            "taxes", "forex", "budgeting", "financial literacy", "capital", 
            "dividends", "portfolio", "risk management"
        ],
        "education": [
            "school", "university", "learning", "education", "online courses", 
            "teaching", "research", "academic", "students", "tutoring", 
            "educational resources", "training", "workshops", "professional development", 
            "curriculum", "classroom", "e-learning", "adult education", "vocational", 
            "literacy", "scholarship", "study skills", "mentorship", "education technology"
        ],
        "sports": [
            "football", "basketball", "cricket", "sports", "athlete", "tournament", 
            "fitness", "exercise", "training", "coaching", "team", "competition", 
            "Olympics", "World Cup", "fan", "playoffs", "outdoor activities", 
            "marathon", "swimming", "gymnastics", "sports science", "nutrition", 
            "esports", "athletic gear", "sporting events"
        ],
        "entertainment": [
            "movies", "music", "tv", "series", "celebrities", "media", 
            "hollywood", "streaming", "theater", "concert", "comedy", "pop culture", 
            "podcasts", "reviews", "critics", "book", "novel", "documentary", 
            "video games", "art", "fashion", "celebrity news", "fan fiction"
        ],
        "travel": [
            "travel", "tourism", "adventure", "hotels", "flights", "vacation", 
            "beaches", "destinations", "backpacking", "road trips", "culture", 
            "sightseeing", "itinerary", "travel tips", "holiday", "expedition", 
            "wildlife", "cruise", "travel photography", "travel blogs", "eco-tourism", 
            "travel insurance", "local cuisine"
        ],
        "food": [
            "cooking", "recipes", "cuisine", "restaurants", "dishes", "gourmet", 
            "food", "chefs", "baking", "meal prep", "nutrition", "vegetarian", 
            "vegan", "gluten-free", "food blogs", "gastronomy", "food trends", 
            "catering", "food safety", "farm-to-table", "food photography"
        ],
        "politics": [
            "government", "policy", "elections", "politicians", "democracy", 
            "law", "international relations", "political parties", "campaigns", 
            "voting", "activism", "human rights", "legislation", "diplomacy", 
            "political analysis", "political theory", "social issues", 
            "political commentary", "citizen engagement", "national security"
        ],
        "science": [
            "science", "research", "experiments", "theory", "physics", "chemistry", 
            "biology", "astronomy", "ecology", "genetics", "microbiology", 
            "environmental science", "scientific method", "data analysis", 
            "laboratory", "field studies", "innovation", "scientific community", 
            "peer review", "science communication", "science policy"
        ],
        "fashion": [
            "fashion", "style", "trends", "clothing", "accessories", "runway", 
            "designer", "beauty", "makeup", "cosmetics", "streetwear", 
            "sustainable fashion", "fashion journalism", "vintage", "wardrobe", 
            "personal style", "fashion history", "fashion shows", "fashion photography"
        ],
        "automotive": [
            "cars", "automobiles", "motorcycles", "vehicles", "transportation", 
            "driving", "road safety", "car maintenance", "electric vehicles", 
            "hybrid cars", "auto industry", "car reviews", "car technology", 
            "racing", "automotive news", "traffic", "insurance", "car accessories"
        ],
        "real estate": [
            "real estate", "property", "housing", "investment", "realty", 
            "mortgage", "buying", "selling", "leasing", "renting", "housing market", 
            "interior design", "real estate investment trusts", "commercial real estate", 
            "property management", "real estate agent", "home improvement", 
            "landscaping", "open house", "real estate trends"
        ],
        "saas": [
            "saas", "software as a service", "cloud computing", "subscription model", 
            "platform as a service", "application hosting", "web applications", 
            "SaaS solutions", "API", "integration", "multi-tenancy", 
            "customer relationship management", "CRM", "enterprise resource planning", 
            "ERP", "marketing automation", "project management", "collaboration tools", 
            "remote work", "analytics", "data storage", "business intelligence", 
            "user experience", "scalability", "software deployment", "devops", 
            "cybersecurity", "data protection", "compliance", "user management", 
            "digital transformation", "IT service management", "customer support software",
            "HR management software", "e-commerce platforms", "payment processing", 
            "content management systems", "SaaS metrics", "churn rate", "onboarding", 
            "self-service", "freemium", "cloud infrastructure", "data visualization", 
            "software updates", "bug tracking", "collaboration", "workflow automation"
        ],
        "chat_software": [
            "chat software", "messaging", "instant messaging", "chat application", 
            "live chat", "customer support", "chatbots", "AI chatbots", 
            "real-time messaging", "communication tools", "team collaboration", 
            "video conferencing", "audio calls", "text chat", "group chat", 
            "social messaging", "mobile messaging", "desktop chat", 
            "end-to-end encryption", "privacy", "user authentication", 
            "message notifications", "chat integration", "API for chat", 
            "customer engagement", "user feedback", "help desk software", 
            "ticketing system", "CRM integration", "multichannel support", 
            "chat analytics", "bot training", "natural language processing", 
            "knowledge base", "self-service support", "FAQ bot", 
            "web chat", "SMS chat", "whatsapp integration", "slack integration"
        ]
    }
