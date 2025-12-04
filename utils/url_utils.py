from urllib.parse import urlparse, urljoin, quote
import re

def normalize_url(url):
    """
    Normalize URL by removing fragments and query parameters
    
    Args:
        url (str): URL to normalize
    
    Returns:
        str: Normalized URL
    """
    parsed = urlparse(url)
    # Remove fragment and query params
    normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    # Remove trailing slash unless it's root
    if normalized.endswith('/') and len(parsed.path) > 1:
        normalized = normalized[:-1]
    return normalized

def is_same_domain(url1, url2):
    """
    Check if two URLs are from the same domain
    
    Args:
        url1 (str): First URL
        url2 (str): Second URL
    
    Returns:
        bool: True if same domain
    """
    domain1 = urlparse(url1).netloc
    domain2 = urlparse(url2).netloc
    return domain1 == domain2

def get_url_keywords(url):
    """
    Extract potential keywords from URL path
    
    Args:
        url (str): URL to analyze
    
    Returns:
        list: List of potential keywords
    """
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Remove common web extensions
    path = re.sub(r'\.(html|htm|php|asp|jsp)$', '', path)
    
    # Split by common separators
    keywords = re.split(r'[/_\-.]', path)
    
    # Filter out empty strings and common words
    common_words = {'www', 'index', 'home', 'page', 'default', 'main'}
    keywords = [k for k in keywords if k and k not in common_words and len(k) > 2]
    
    return keywords

def find_relevant_urls(links, question_keywords):
    """
    Find URLs most likely to contain relevant information
    
    Args:
        links (list): List of link dictionaries with 'url' and 'text'
        question_keywords (list): Keywords from user question
    
    Returns:
        list: Sorted list of relevant URLs
    """
    scored_urls = []
    
    for link in links:
        score = 0
        url = link['url'].lower()
        text = link['text'].lower()
        
        # Score based on keywords in URL path
        url_keywords = get_url_keywords(url)
        for keyword in question_keywords:
            if any(keyword.lower() in uk for uk in url_keywords):
                score += 3
        
        # Score based on keywords in link text
        for keyword in question_keywords:
            if keyword.lower() in text:
                score += 2
        
        # Boost score for certain helpful pages
        helpful_indicators = [
            'support', 'help', 'faq', 'contact', 'about', 
            'policy', 'return', 'refund', 'shipping', 
            'product', 'service', 'documentation', 'guide'
        ]
        
        for indicator in helpful_indicators:
            if indicator in url or indicator in text:
                score += 1
        
        if score > 0:
            scored_urls.append({
                'url': link['url'],
                'text': link['text'],
                'score': score
            })
    
    # Sort by score (highest first)
    scored_urls.sort(key=lambda x: x['score'], reverse=True)
    
    return scored_urls

def extract_question_keywords(question):
    """
    Extract key terms from user question
    
    Args:
        question (str): User's question
    
    Returns:
        list: List of important keywords
    """
    # Remove common question words
    stop_words = {
        'how', 'what', 'where', 'when', 'why', 'who', 'which', 'can', 'could', 
        'would', 'should', 'do', 'does', 'did', 'is', 'are', 'was', 'were',
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'around'
    }
    
    # Clean and split question
    question_clean = re.sub(r'[^\w\s]', '', question.lower())
    words = question_clean.split()
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 2]
    
    return keywords

def prioritize_navigation_strategy(current_url, question_keywords, available_links):
    """
    Suggest navigation strategy based on current context
    
    Args:
        current_url (str): Current page URL
        question_keywords (list): Keywords from question
        available_links (list): Available links to navigate to
    
    Returns:
        dict: Strategy recommendation
    """
    # Get current page context
    current_keywords = get_url_keywords(current_url)
    
    # Find most relevant next URLs
    relevant_urls = find_relevant_urls(available_links, question_keywords)
    
    strategy = {
        'current_page_relevance': any(kw in current_keywords for kw in question_keywords),
        'recommended_urls': relevant_urls[:3],  # Top 3 recommendations
        'reasoning': []
    }
    
    if not strategy['current_page_relevance']:
        strategy['reasoning'].append("Current page doesn't seem directly relevant to the question")
    
    if relevant_urls:
        strategy['reasoning'].append(f"Found {len(relevant_urls)} potentially relevant pages")
    else:
        strategy['reasoning'].append("No obviously relevant pages found, may need to explore systematically")
    
    return strategy

if __name__ == "__main__":
    # Test the utilities
    test_question = "How do I get a refund for Product A?"
    keywords = extract_question_keywords(test_question)
    print(f"Keywords: {keywords}")
    
    test_links = [
        {'url': 'https://example.com/support/returns', 'text': 'Returns Policy'},
        {'url': 'https://example.com/products/product-a', 'text': 'Product A Details'},
        {'url': 'https://example.com/contact', 'text': 'Contact Us'}
    ]
    
    relevant = find_relevant_urls(test_links, keywords)
    print(f"Relevant URLs: {[r['url'] for r in relevant]}")