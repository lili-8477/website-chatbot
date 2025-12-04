from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from flow import run_chatbot
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Website Chatbot API",
    description="An intelligent chatbot that dynamically crawls websites to answer questions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    question: str
    website_url: str

class ChatResponse(BaseModel):
    answer: str
    status: str
    pages_visited: int
    urls_explored: list

class ConfigRequest(BaseModel):
    website_url: str

# Global configuration
config = {
    "default_website_url": os.getenv("DEFAULT_WEBSITE_URL", "https://example.com")
}

@app.get("/api")
async def read_root():
    """Health check endpoint"""
    return {
        "message": "Website Chatbot API is running",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "api": "operational",
        "default_website": config["default_website_url"]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chatbot endpoint that processes user questions
    """
    try:
        logger.info(f"Processing question: {request.question}")
        logger.info(f"Target website: {request.website_url}")
        
        # Validate inputs
        if not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        if not request.website_url.strip():
            raise HTTPException(status_code=400, detail="Website URL cannot be empty")
        
        # Ensure URL has protocol
        website_url = request.website_url
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
        
        # Run the chatbot flow
        result = run_chatbot(request.question, website_url)
        
        # Extract information from the result
        final_answer = result.get("final_answer", "I couldn't generate an answer.")
        visited_urls = result.get("visited_urls", set())
        url_content = result.get("url_content", {})
        
        # Compile list of explored URLs
        explored_urls = []
        for url_idx in visited_urls:
            if url_idx in url_content:
                content_data = url_content[url_idx]
                explored_urls.append({
                    "url": content_data["url"],
                    "title": content_data["title"]
                })
        
        logger.info(f"Successfully processed question. Visited {len(visited_urls)} pages.")
        
        return ChatResponse(
            answer=final_answer,
            status="success",
            pages_visited=len(visited_urls),
            urls_explored=explored_urls
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing your request: {str(e)}"
        )

@app.post("/configure")
async def configure_website(request: ConfigRequest):
    """
    Configure the default website URL
    """
    try:
        website_url = request.website_url
        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url
            
        config["default_website_url"] = website_url
        
        return {
            "message": "Configuration updated successfully",
            "default_website_url": website_url
        }
        
    except Exception as e:
        logger.error(f"Error configuring website: {str(e)}")
        raise HTTPException(status_code=500, detail="Configuration failed")

@app.get("/config")
async def get_config():
    """Get current configuration"""
    return config

# Mount static files (for serving the frontend)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the frontend HTML at root path
@app.get("/", include_in_schema=False)
async def serve_frontend():
    """Serve the main frontend HTML file"""
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    # For development - in production, use proper WSGI server
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level="info"
    )