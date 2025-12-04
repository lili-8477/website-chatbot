import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_website(url, timeout=None):
    """
    Scrape website content and extract text and links
    
    Args:
        url (str): URL to scrape
        timeout (int): Request timeout in seconds (defaults to env var or 10)
    
    Returns:
        dict: Contains 'content', 'links', 'title', 'error'
    """
    if timeout is None:
        timeout = int(os.getenv("REQUEST_TIMEOUT", "10"))
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Extract title
        title = soup.title.string if soup.title else "No title"
        title = title.strip()
        
        # Extract text content
        content = soup.get_text()
        # Clean up whitespace
        content = re.sub(r'\s+', ' ', content).strip()
        
        # Extract links
        links = []
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative URLs to absolute
            absolute_url = urljoin(url, href)
            
            # Only include same-domain links
            if urlparse(absolute_url).netloc == urlparse(url).netloc:
                link_text = link.get_text().strip()
                if link_text and absolute_url not in [l['url'] for l in links]:
                    links.append({
                        'url': absolute_url,
                        'text': link_text
                    })
        
        return {
            'url': url,
            'title': title,
            'content': content[:5000],  # Limit content length
            'links': links[:20],  # Limit number of links
            'error': None
        }
        
    except requests.RequestException as e:
        return {
            'url': url,
            'title': None,
            'content': None,
            'links': [],
            'error': f"Request failed: {str(e)}"
        }
    except Exception as e:
        return {
            'url': url,
            'title': None,
            'content': None,
            'links': [],
            'error': f"Parsing failed: {str(e)}"
        }

def extract_relevant_content(content, keywords):
    """
    Extract content most relevant to given keywords
    
    Args:
        content (str): Full page content
        keywords (list): List of keywords to search for
    
    Returns:
        str: Most relevant content sections
    """
    if not content or not keywords:
        return content
    
    sentences = content.split('.')
    relevant_sentences = []
    
    for sentence in sentences:
        sentence = sentence.strip()
        if any(keyword.lower() in sentence.lower() for keyword in keywords):
            relevant_sentences.append(sentence)
    
    if relevant_sentences:
        return '. '.join(relevant_sentences)
    
    # If no exact matches, return first part of content
    return content[:1000]

if __name__ == "__main__":
    # Test the scraper
    test_url = "https://example.com"
    result = scrape_website(test_url)
    print(f"Title: {result['title']}")
    print(f"Content preview: {result['content'][:200]}...")
    print(f"Found {len(result['links'])} links")
    if result['error']:
        print(f"Error: {result['error']}")