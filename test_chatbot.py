#!/usr/bin/env python3
"""
Simple test script to validate the chatbot functionality
"""
import os
from dotenv import load_dotenv
from flow import run_chatbot

# Load environment variables
load_dotenv()

def test_basic_functionality():
    """Test basic chatbot functionality with a simple question"""
    
    # Check OpenAI API key
    if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
        print("⚠️  Warning: OPENAI_API_KEY not properly set. Please update your .env file.")
        return False
    
    print("🤖 Testing Website Chatbot...")
    print("-" * 50)
    
    # Test with a public website
    test_question = "What is this website about?"
    test_website = "https://httpbin.org"  # Simple test site with reliable content
    
    print(f"Question: {test_question}")
    print(f"Website: {test_website}")
    print("\n📡 Starting crawl process...")
    
    try:
        # Run the chatbot
        result = run_chatbot(test_question, test_website)
        
        # Print results
        print("\n✅ Results:")
        print(f"Pages visited: {len(result.get('visited_urls', []))}")
        print(f"URLs discovered: {len(result.get('all_discovered_urls', []))}")
        print(f"Content collected: {len(result.get('url_content', {}))}")
        
        final_answer = result.get('final_answer')
        if final_answer:
            print(f"\n🎯 Final Answer:\n{final_answer}")
            return True
        else:
            print("❌ No final answer generated")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

def test_utilities():
    """Test individual utility functions"""
    print("\n🔧 Testing utility functions...")
    
    try:
        from utils.url_utils import extract_question_keywords, normalize_url
        from utils.web_scraper import scrape_website
        
        # Test keyword extraction
        keywords = extract_question_keywords("How do I return a product?")
        print(f"✅ Keywords extracted: {keywords}")
        
        # Test URL normalization
        normalized = normalize_url("https://example.com/page/")
        print(f"✅ URL normalized: {normalized}")
        
        # Test web scraping (basic test)
        print("📡 Testing web scraper...")
        result = scrape_website("https://httpbin.org", timeout=5)
        
        if result['error']:
            print(f"⚠️  Scraping test returned error: {result['error']}")
        else:
            print(f"✅ Scraping successful: {result['title'][:50]}...")
            
        return True
        
    except Exception as e:
        print(f"❌ Utility test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Website Chatbot Tests")
    print("=" * 50)
    
    # Test utilities first
    utils_ok = test_utilities()
    
    # Test main functionality if utils work
    if utils_ok:
        main_ok = test_basic_functionality()
        
        if main_ok:
            print("\n🎉 All tests passed! Your chatbot is ready.")
            print("\n📝 To run the server:")
            print("   python main.py")
            print("\n🌐 Then visit: http://localhost:8000")
        else:
            print("\n⚠️  Some tests failed. Check your configuration.")
    else:
        print("\n❌ Utility tests failed. Check your imports and dependencies.")

if __name__ == "__main__":
    main()