from pocketflow import Node
from utils.call_llm import call_llm
from utils.web_scraper import scrape_website, extract_relevant_content
from utils.url_utils import extract_question_keywords, find_relevant_urls, prioritize_navigation_strategy
import yaml

class CrawlAndExtract(Node):
    """
    Node that crawls web pages and extracts content
    """
    
    def prep(self, shared):
        """Get the next URL to process from the queue"""
        urls_to_process = shared.get("urls_to_process", [])
        
        if not urls_to_process:
            return None
            
        # Get the next URL index to process
        url_index = urls_to_process[0]
        all_urls = shared.get("all_discovered_urls", [])
        
        if url_index >= len(all_urls):
            return None
            
        return {
            "url_index": url_index,
            "url": all_urls[url_index],
            "question_keywords": shared.get("question_keywords", [])
        }
    
    def exec(self, prep_res):
        """Scrape the website and extract content"""
        if not prep_res:
            return None
            
        url = prep_res["url"]
        question_keywords = prep_res["question_keywords"]
        
        # Scrape the website
        result = scrape_website(url)
        
        if result["error"]:
            return {
                "url_index": prep_res["url_index"],
                "url": url,
                "error": result["error"],
                "content": None,
                "links": [],
                "title": None
            }
        
        # Extract relevant content based on question keywords
        relevant_content = extract_relevant_content(result["content"], question_keywords)
        
        return {
            "url_index": prep_res["url_index"],
            "url": url,
            "title": result["title"],
            "content": relevant_content,
            "links": result["links"],
            "error": None
        }
    
    def post(self, shared, prep_res, exec_res):
        """Store the extracted content and update discovered URLs"""
        if not exec_res:
            return "agent_decide"
        
        url_index = exec_res["url_index"]
        
        # Remove this URL from processing queue
        urls_to_process = shared.get("urls_to_process", [])
        if url_index in urls_to_process:
            urls_to_process.remove(url_index)
            shared["urls_to_process"] = urls_to_process
        
        # Mark as visited
        visited_urls = shared.get("visited_urls", set())
        visited_urls.add(url_index)
        shared["visited_urls"] = visited_urls
        
        # Store content if successfully scraped
        if exec_res["content"]:
            url_content = shared.get("url_content", {})
            url_content[url_index] = {
                "url": exec_res["url"],
                "title": exec_res["title"],
                "content": exec_res["content"]
            }
            shared["url_content"] = url_content
            
            # Add newly discovered URLs
            all_discovered_urls = shared.get("all_discovered_urls", [])
            for link in exec_res["links"]:
                if link["url"] not in all_discovered_urls:
                    all_discovered_urls.append(link["url"])
            shared["all_discovered_urls"] = all_discovered_urls
        
        return "agent_decide"

class AgentDecision(Node):
    """
    Agent node that decides whether to explore more or provide an answer
    """
    
    def prep(self, shared):
        """Prepare context for agent decision"""
        user_question = shared.get("user_question", "")
        question_keywords = shared.get("question_keywords", [])
        url_content = shared.get("url_content", {})
        visited_urls = shared.get("visited_urls", set())
        all_discovered_urls = shared.get("all_discovered_urls", [])
        urls_to_process = shared.get("urls_to_process", [])
        
        # Compile collected information
        collected_info = []
        for url_idx, content_data in url_content.items():
            collected_info.append({
                "url": content_data["url"],
                "title": content_data["title"],
                "content": content_data["content"][:500]  # Truncate for context
            })
        
        # Find potential next URLs
        available_links = []
        if all_discovered_urls and visited_urls:
            for i, url in enumerate(all_discovered_urls):
                if i not in visited_urls:
                    available_links.append({"url": url, "text": url})
        
        return {
            "question": user_question,
            "keywords": question_keywords,
            "collected_info": collected_info,
            "available_links": available_links[:10],  # Limit to 10
            "visited_count": len(visited_urls),
            "pending_urls": len(urls_to_process)
        }
    
    def exec(self, prep_res):
        """Make decision about next action"""
        if not prep_res:
            return {"action": "answer", "reason": "No data to process"}
        
        question = prep_res["question"]
        collected_info = prep_res["collected_info"]
        available_links = prep_res["available_links"]
        visited_count = prep_res["visited_count"]
        
        # Create context summary
        info_summary = "\n".join([
            f"Page: {info['title']} ({info['url']})\nContent: {info['content']}\n"
            for info in collected_info
        ])
        
        available_urls = "\n".join([f"- {link['url']}" for link in available_links[:5]])
        
        prompt = f"""
You are a web research agent. Analyze the current situation and decide the next action.

QUESTION: {question}

INFORMATION COLLECTED SO FAR:
{info_summary if info_summary else "No information collected yet."}

AVAILABLE URLS TO EXPLORE:
{available_urls if available_urls else "No more URLs available."}

CURRENT STATUS:
- Pages visited: {visited_count}
- Available unvisited URLs: {len(available_links)}

DECISION CRITERIA:
1. If you have sufficient information to answer the question comprehensively, choose "answer"
2. If you need more specific information and there are relevant URLs available, choose "explore" 
3. If you've visited 5+ pages without finding relevant info, choose "answer"
4. If no more URLs are available, choose "answer"

Choose your action and provide reasoning:

```yaml
action: explore  # or "answer"
reasoning: |
  Explain why you chose this action based on the information available
  and what you're looking for
next_url: |
  If action is "explore", specify which URL from available URLs seems most promising
  and why. Just provide the URL.
```"""

        response = call_llm(prompt)
        
        try:
            # Extract YAML from response
            yaml_start = response.find("```yaml")
            yaml_end = response.find("```", yaml_start + 7)
            
            if yaml_start != -1 and yaml_end != -1:
                yaml_content = response[yaml_start + 7:yaml_end].strip()
                result = yaml.safe_load(yaml_content)
            else:
                # Fallback parsing
                result = {"action": "answer", "reasoning": "Failed to parse decision"}
            
            # Validate result
            if "action" not in result or result["action"] not in ["explore", "answer"]:
                result["action"] = "answer"
                
            return result
            
        except Exception as e:
            return {
                "action": "answer",
                "reasoning": f"Error parsing decision: {str(e)}"
            }
    
    def post(self, shared, prep_res, exec_res):
        """Process the agent's decision"""
        action = exec_res.get("action", "answer")
        
        if action == "explore":
            # Find the next URL to explore
            next_url = exec_res.get("next_url", "").strip()
            all_discovered_urls = shared.get("all_discovered_urls", [])
            
            # Find the index of the next URL
            next_url_index = None
            for i, url in enumerate(all_discovered_urls):
                if next_url in url or url in next_url:
                    next_url_index = i
                    break
            
            if next_url_index is not None:
                urls_to_process = shared.get("urls_to_process", [])
                visited_urls = shared.get("visited_urls", set())
                
                if next_url_index not in visited_urls and next_url_index not in urls_to_process:
                    urls_to_process.append(next_url_index)
                    shared["urls_to_process"] = urls_to_process
                    return "explore"
        
        # Default to answer if we can't explore or chose to answer
        return "answer"

class DraftAnswer(Node):
    """
    Node that creates the final answer based on collected information
    """
    
    def prep(self, shared):
        """Prepare all collected information for final answer"""
        user_question = shared.get("user_question", "")
        url_content = shared.get("url_content", {})
        
        # Compile all content
        all_content = []
        for url_idx, content_data in url_content.items():
            all_content.append({
                "url": content_data["url"],
                "title": content_data["title"],
                "content": content_data["content"]
            })
        
        return {
            "question": user_question,
            "content": all_content
        }
    
    def exec(self, prep_res):
        """Generate comprehensive answer"""
        if not prep_res:
            return "I couldn't find any information to answer your question."
        
        question = prep_res["question"]
        content = prep_res["content"]
        
        if not content:
            return "I couldn't find any relevant information on the website to answer your question."
        
        # Create context from all collected content
        context_parts = []
        for item in content:
            context_parts.append(f"From {item['title']} ({item['url']}):\n{item['content']}\n")
        
        full_context = "\n---\n".join(context_parts)
        
        prompt = f"""
Based on the information I gathered from the website, please provide a comprehensive answer to the user's question.

QUESTION: {question}

INFORMATION FROM WEBSITE:
{full_context}

Please provide a helpful, accurate answer based on the information above. If the information is incomplete, mention what additional details might be needed. Structure your answer clearly and reference relevant information from the pages when appropriate.

ANSWER:"""

        return call_llm(prompt)
    
    def post(self, shared, prep_res, exec_res):
        """Store the final answer"""
        shared["final_answer"] = exec_res
        print(f"\nFINAL ANSWER:\n{exec_res}\n")