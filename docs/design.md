# Design Doc: Website Chatbot

## Requirements

Build an intelligent website chatbot that dynamically crawls websites to answer user questions. The bot acts like a focused intern that reads website content in real-time to provide comprehensive answers.

**User Stories:**
- As a user, I want to ask questions about any website and get accurate answers based on current content
- As a user, I want the bot to intelligently navigate through multiple pages to gather complete information
- As a user, I want to see what pages the bot explored to build trust in the answer
- As a user, I want a simple web interface to interact with the chatbot

## Flow Design

### Applicable Design Pattern: Agent

The chatbot uses an **Agent** design pattern where the system autonomously decides whether to explore more content or provide an answer based on current information.

**Agent Context:**
- User question and extracted keywords
- Previously crawled page content
- Available URLs discovered during crawling
- Current exploration state (pages visited, pending URLs)

**Agent Action Space:**
- `explore`: Navigate to and scrape a new URL for more information
- `answer`: Generate final response based on collected information

### Flow High-level Design:

1. **CrawlAndExtract Node**: Fetches and extracts content from URLs, discovers new links
2. **AgentDecision Node**: Analyzes collected information and decides next action
3. **DraftAnswer Node**: Generates comprehensive final answer from all collected content

```mermaid
flowchart TD
    start[User Question + Website URL] --> crawl[CrawlAndExtract]
    crawl --> agent[AgentDecision]
    agent -->|explore| crawl
    agent -->|answer| draft[DraftAnswer]
    draft --> end[Final Answer]
```

## Utility Functions

1. **Web Scraper** (`utils/web_scraper.py`)
   - *Input*: URL string
   - *Output*: Dict with content, links, title, and error status
   - *Purpose*: Scrape webpage content and extract text and internal links

2. **URL Utilities** (`utils/url_utils.py`)
   - *Input*: URLs, question text
   - *Output*: Processed URLs, keyword lists, relevance scores
   - *Purpose*: Normalize URLs, extract keywords, find relevant navigation paths

3. **Call LLM** (`utils/call_llm.py`)
   - *Input*: Prompt string
   - *Output*: LLM response string
   - *Purpose*: Interface with OpenAI GPT-4 for agent decisions and answer generation

## Node Design

### Shared Store

The shared store maintains the complete state of the crawling session:

```python
shared = {
    "user_question": "How do I get a refund?",
    "question_keywords": ["refund", "return", "policy"],
    "urls_to_process": [1, 3],  # Queue of URL indices to crawl
    "visited_urls": {0, 2},     # Set of already crawled URL indices
    "url_content": {            # Stored content from crawled pages
        0: {"url": "...", "title": "...", "content": "..."},
        2: {"url": "...", "title": "...", "content": "..."}
    },
    "all_discovered_urls": ["https://site.com", "https://site.com/support", ...],
    "final_answer": None
}
```

### Node Steps

1. **CrawlAndExtract Node**
   - *Purpose*: Fetch webpage content and extract relevant information
   - *Type*: Regular Node
   - *Steps*:
     - *prep*: Get next URL from processing queue and question keywords
     - *exec*: Scrape website, extract content and links, filter for relevance
     - *post*: Store content, update discovered URLs, mark as visited, return "agent_decide"

2. **AgentDecision Node**
   - *Purpose*: Decide whether to explore more content or generate answer
   - *Type*: Regular Node  
   - *Steps*:
     - *prep*: Compile collected information and available next URLs
     - *exec*: Use LLM to analyze context and decide next action (explore/answer)
     - *post*: Queue next URL for exploration or proceed to answer generation

3. **DraftAnswer Node**
   - *Purpose*: Generate comprehensive final answer from all collected content
   - *Type*: Regular Node
   - *Steps*:
     - *prep*: Gather all collected content from crawled pages
     - *exec*: Use LLM to synthesize information into comprehensive answer
     - *post*: Store final answer and display result

## Architecture

**Backend**: FastAPI with the following endpoints:
- `POST /chat`: Main chatbot interaction
- `POST /configure`: Set target website URL  
- `GET /config`: Get current configuration
- `GET /health`: Health check
- `GET /`: Serve frontend interface

**Frontend**: HTML/CSS/JavaScript single-page application with:
- Chat interface for user interactions
- Website URL configuration panel
- Real-time status indicators
- Progress tracking during crawl operations

**Integration**: The FastAPI backend integrates the PocketFlow agent and serves both API endpoints and the frontend interface.