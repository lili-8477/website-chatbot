from pocketflow import Flow
from nodes import CrawlAndExtract, AgentDecision, DraftAnswer
from utils.url_utils import extract_question_keywords

def create_chatbot_flow():
    """Create and return the website chatbot flow."""
    # Create nodes
    crawl_node = CrawlAndExtract()
    agent_node = AgentDecision() 
    draft_answer_node = DraftAnswer()
    
    # Connect nodes with actions
    crawl_node - "agent_decide" >> agent_node
    agent_node - "explore" >> crawl_node    # Loop back to crawl more
    agent_node - "answer" >> draft_answer_node  # Generate final answer
    
    # Create flow starting with crawl node
    return Flow(start=crawl_node)

def initialize_shared_store(user_question, base_url):
    """
    Initialize the shared store with the user question and starting URL
    
    Args:
        user_question (str): The user's question
        base_url (str): The website's base URL to start crawling from
    
    Returns:
        dict: Initialized shared store
    """
    question_keywords = extract_question_keywords(user_question)
    
    shared = {
        "user_question": user_question,
        "question_keywords": question_keywords,
        "urls_to_process": [0],  # Start with index 0 (base URL)
        "visited_urls": set(),
        "url_content": {},  # {url_index: {"url": "", "title": "", "content": ""}}
        "all_discovered_urls": [base_url],  # Master list of URLs
        "final_answer": None
    }
    
    return shared

def run_chatbot(user_question, base_url):
    """
    Run the complete chatbot flow
    
    Args:
        user_question (str): User's question
        base_url (str): Website base URL to crawl
    
    Returns:
        dict: Final shared store with answer
    """
    # Initialize shared store
    shared = initialize_shared_store(user_question, base_url)
    
    # Create and run flow
    chatbot_flow = create_chatbot_flow()
    chatbot_flow.run(shared)
    
    return shared

# Create the main chatbot flow instance
chatbot_flow = create_chatbot_flow()

if __name__ == "__main__":
    # Example usage
    question = "How do I get a refund?"
    website = "https://example.com"
    
    result = run_chatbot(question, website)
    print(f"Final answer: {result['final_answer']}")