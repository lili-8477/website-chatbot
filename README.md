# 🤖 Website Chatbot

An intelligent chatbot that dynamically crawls websites to answer user questions in real-time. 

## ✨ Live Demo

🔗 **Try it live**: [https://website-chatbot.ai-builders.space](https://website-chatbot.ai-builders.space) *(Available after deployment)*

## 🚀 Features

- **🧠 Intelligent Agent**: Uses PocketFlow's agent pattern to make smart decisions about when to explore vs. answer
- **🔍 Dynamic Website Crawling**: Reads websites in real-time, navigating through multiple pages to find relevant information
- **🎯 Context-Aware Responses**: Provides comprehensive answers based on actual website content
- **⚡ Real-time Web Interface**: Clean, responsive chat interface with live status updates
- **🔗 Multi-page Analysis**: Intelligently explores multiple pages when needed for complete answers
- **📊 Transparent Process**: Shows exactly which pages were explored for each answer
- **🐳 Docker Ready**: Optimized for deployment on ai-builders.space platform

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lili-8477/website-chatbot.git
cd website-chatbot
```

### 2. Automated Setup

```bash
python setup.py
```

This script will:
- ✅ Check Python version compatibility (3.8+)
- ✅ Install all dependencies
- ✅ Create .env file from template
- ✅ Validate the installation

### 3. Configure API Key

Edit the `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your-openai-api-key-here
DEFAULT_WEBSITE_URL=https://github.com/langchain-ai/agent-chat-ui
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

### 4. Run the Application

```bash
python main.py
```

Open your browser and go to: **http://localhost:8000**

## 🎮 How to Use

1. **Set Website URL**: Enter any website URL in the configuration panel
2. **Ask Questions**: Type questions about the website content
3. **Watch the Magic**: The agent will intelligently crawl the site to find answers
4. **Get Comprehensive Answers**: Receive detailed responses based on multiple pages if needed

### Example Questions to Try

- "What is this website about?"
- "How do I get started?"
- "What are the main features?"
- "Do you have documentation?"
- "What are the pricing options?"

## 🏗️ Architecture

The chatbot implements PocketFlow's **Agent Design Pattern**:

```mermaid
flowchart TD
    start[User Question] --> crawl[CrawlAndExtract Node]
    crawl --> agent[AgentDecision Node]
    agent -->|🔍 explore| crawl
    agent -->|💬 answer| draft[DraftAnswer Node]
    draft --> end[📝 Final Answer]
    
    style agent fill:#e1f5fe
    style crawl fill:#f3e5f5
    style draft fill:#e8f5e8
```

### Key Components

1. **🔍 CrawlAndExtract Node**
   - Scrapes web pages and extracts clean content
   - Finds relevant links based on question keywords
   - Handles various content types (HTML, text, etc.)

2. **🧠 AgentDecision Node**
   - Uses GPT to make intelligent decisions
   - Decides whether to explore more pages or answer
   - Considers collected context and question complexity

3. **📝 DraftAnswer Node**
   - Generates comprehensive final answers
   - Synthesizes information from multiple pages
   - Provides transparent source attribution

4. **⚡ FastAPI Backend**
   - Single-process architecture serving both API and static files
   - RESTful endpoints with proper error handling
   - Health checks and monitoring

5. **🎨 Frontend Interface**
   - Responsive design with real-time updates
   - Progress indicators and status messages
   - Clean, intuitive user experience

## 📡 API Reference

### Chat Endpoint

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What are the main features?",
       "website_url": "https://example.com"
     }'
```

**Response:**
```json
{
  "answer": "Detailed answer based on website content...",
  "status": "success",
  "pages_visited": 2,
  "urls_explored": [
    {
      "url": "https://example.com",
      "title": "Home Page"
    },
    {
      "url": "https://example.com/features",
      "title": "Features"
    }
  ]
}
```

### Other Endpoints

- `GET /` - Web interface
- `GET /health` - Health check
- `POST /configure` - Set default website URL
- `GET /config` - Get current configuration

## 🐳 Docker Deployment

### Local Testing

```bash
# Build and run locally
docker build -t website-chatbot .
docker run -p 8000:8000 \
  -e PORT=8000 \
  -e OPENAI_API_KEY=your-key \
  website-chatbot
```

Test the deployment:
```bash
# Health check
curl http://localhost:8000/health

# Test chat functionality
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?", "website_url": "https://github.com/langchain-ai/agent-chat-ui"}'
```

### 🚀 AI Builders Space Deployment

This project is optimized for deployment on ai-builders.space platform:

#### Prerequisites Check

Run the deployment readiness checker:

```bash
python check_deployment_ready.py
```

This will verify:
- ✅ Dockerfile configuration
- ✅ Environment variables setup
- ✅ Static files structure
- ✅ Requirements.txt completeness
- ✅ Git repository status
- ✅ Security configurations

#### Deployment Information Needed

1. **GitHub Repository URL**: `https://github.com/lili-8477/website-chatbot`
2. **Service Name**: `website-chatbot` (or your preferred name)
3. **Git Branch**: `main`

#### Platform Features

- 🏗️ **Optimized Architecture**: Single process serving both API and static files
- 💾 **Memory Efficient**: Designed for 256MB RAM limit
- ⚙️ **Environment Variables**: Automatic PORT configuration
- 🔒 **Security**: Non-root user and secure defaults
- 📊 **Health Monitoring**: Built-in health check endpoints
- 🔄 **Auto-scaling**: Platform handles traffic spikes

#### Deployment Steps

1. **Commit all changes** to your repository:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Contact your instructor** or use the deployment API with:
   - Repository URL: `https://github.com/lili-8477/website-chatbot`
   - Service name: `website-chatbot`
   - Branch: `main`

3. **Wait 5-10 minutes** for provisioning

4. **Access your deployed chatbot** at:
   `https://website-chatbot.ai-builders.space`

## 📂 Project Structure

```
website-chatbot/
├── 📄 main.py                 # FastAPI application entry point
├── 🔄 flow.py                 # PocketFlow workflow definition
├── 🧩 nodes.py                # Agent node implementations
├── 📋 requirements.txt        # Python dependencies
├── 🧪 test_chatbot.py        # Test script
├── 🔧 setup.py               # Automated setup script
├── 🐳 Dockerfile             # Container configuration
├── ✅ check_deployment_ready.py # Deployment validator
├── ⚙️  .env.example           # Environment template
├── 🎨 static/                 # Web interface
│   ├── 📄 index.html         # Frontend HTML
│   ├── 🎨 style.css          # Styling
│   └── ⚡ script.js          # JavaScript
├── 🔧 utils/                  # Utility functions
│   ├── 🤖 call_llm.py        # OpenAI API wrapper
│   ├── 🕷️  web_scraper.py     # Web scraping
│   └── 🔗 url_utils.py       # URL processing
└── 📚 docs/                   # Documentation
    └── 📋 design.md          # Technical design
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Server Configuration  
HOST=0.0.0.0
PORT=8000

# Application Settings
DEFAULT_WEBSITE_URL=https://example.com
MAX_RETRIES=3
REQUEST_TIMEOUT=10
```

### Advanced Configuration

- **MAX_RETRIES**: Number of retry attempts for failed requests
- **REQUEST_TIMEOUT**: Timeout in seconds for web scraping
- **OPENAI_MODEL**: GPT model to use (gpt-4, gpt-3.5-turbo, etc.)

## 🧪 Testing

Run comprehensive tests:

```bash
# Test utility functions
python test_chatbot.py

# Test individual components
python -c "from utils.web_scraper import scrape_website; print('✅ Web scraper working')"
python -c "from utils.call_llm import call_llm; print('✅ LLM integration working')"

# Test the flow
python -c "from flow import run_chatbot; print('✅ Agent flow working')"
```

## 🎯 Example Use Cases

### E-commerce Support
```
URL: https://shopify.com
Question: "How do I set up payment methods?"
Result: Agent explores pricing, features, and setup pages to provide comprehensive guidance.
```

### Documentation Navigation
```
URL: https://fastapi.tiangolo.com
Question: "How do I handle file uploads?"
Result: Agent finds and synthesizes information from multiple documentation pages.
```

### Company Information
```
URL: https://github.com/microsoft/vscode
Question: "What are the main features of this project?"
Result: Agent reads README, features pages, and documentation to provide detailed overview.
```

## 🛠️ Development

### Adding New Features

1. **New Agent Behaviors**: Modify `nodes.py` AgentDecision logic
2. **Enhanced Scraping**: Extend `utils/web_scraper.py` capabilities
3. **UI Improvements**: Update `static/` files
4. **API Extensions**: Add new endpoints in `main.py`

### Code Quality

- **Linting**: Code follows PEP 8 standards
- **Error Handling**: Comprehensive error handling with retries
- **Logging**: Structured logging for debugging
- **Security**: Input validation and safe URL handling

## 🤝 Contributing

This project demonstrates the PocketFlow framework for building intelligent agents. Contributions welcome:

- 🐛 **Bug Reports**: File issues with detailed descriptions
- ✨ **Feature Requests**: Propose new agent capabilities
- 🔧 **Code Improvements**: Submit PRs with tests
- 📚 **Documentation**: Help improve setup guides

## 📄 License & Credits

Built on the [PocketFlow Project Template](https://github.com/The-Pocket/PocketFlow) for Agentic Coding.

- 📖 [PocketFlow Documentation](https://the-pocket.github.io/PocketFlow/guide.html)
- 🎥 [YouTube Tutorial](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)
- 🤖 Generated with Claude Code

---

**Ready to deploy your intelligent website chatbot? Follow the deployment instructions above!** 🚀