# 🤖 Website Chatbot

An intelligent chatbot that dynamically crawls websites to answer user questions. Built with PocketFlow agent framework and FastAPI.

<p align="center">
  <a href="https://github.com/The-Pocket/PocketFlow" target="_blank">
    <img 
      src="./assets/banner.png" width="800"
    />
  </a>
</p>

## 🚀 Features

- **Intelligent Website Crawling**: Dynamically navigates websites to gather relevant information
- **Agent-Based Decision Making**: Uses PocketFlow's agent pattern to decide when to explore vs. answer
- **Real-time Web Interface**: Clean, responsive chat interface
- **Multi-page Analysis**: Can explore multiple pages to provide comprehensive answers
- **Transparent Process**: Shows which pages were explored for each answer

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- OpenAI API Key

### Quick Setup

Run the automated setup script:

```bash
python setup.py
```

This will:
- Check Python version compatibility
- Install all dependencies
- Create .env file from template
- Validate the installation

Then edit `.env` file and add your OpenAI API key.

### Manual Installation

1. **Clone/Navigate to the project directory**
   ```bash
   cd /path/to/PocketFlow-Template-Python
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Then edit .env file and add your OpenAI API key
   ```

### 🧪 Testing

Run the test script to validate the installation:

```bash
python test_chatbot.py
```

This will test:
- Utility functions (web scraping, URL processing)
- Basic chatbot functionality
- Integration between components

### 🚀 Running the Application

1. **Start the server**
   ```bash
   python main.py
   ```

2. **Open your browser**
   Navigate to: `http://localhost:8000`

3. **Use the chatbot**
   - Set a website URL in the configuration panel
   - Ask questions about the website content
   - Watch as the bot intelligently explores the site to find answers

## 📡 API Endpoints

### Main Endpoints

- `GET /` - Web interface
- `POST /chat` - Chat with the bot
- `POST /configure` - Set target website URL
- `GET /config` - Get current configuration
- `GET /health` - Health check

### Chat API Example

```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What are your refund policies?",
       "website_url": "https://example.com"
     }'
```

## 🏗️ Architecture

The chatbot uses PocketFlow's **Agent** design pattern:

```mermaid
flowchart TD
    start[User Question] --> crawl[CrawlAndExtract Node]
    crawl --> agent[AgentDecision Node]
    agent -->|explore| crawl
    agent -->|answer| draft[DraftAnswer Node]
    draft --> end[Final Answer]
```

### Key Components

1. **CrawlAndExtract Node**: Scrapes web pages and extracts relevant content
2. **AgentDecision Node**: Decides whether to explore more or answer
3. **DraftAnswer Node**: Generates comprehensive final answers
4. **FastAPI Backend**: REST API and web server
5. **HTML/CSS/JS Frontend**: Interactive chat interface

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

- `OPENAI_API_KEY`: Your OpenAI API key (required) - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `DEFAULT_WEBSITE_URL`: Default website to analyze (default: https://example.com)
- `MAX_RETRIES`: Maximum retries for requests (default: 3)
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: 10)

### Default Settings

- **Default Website**: `https://example.com`
- **Server Port**: `8000`
- **Max Pages**: Limited by agent decision-making
- **Timeout**: 10 seconds per page

## 📂 Project Structure

```
project/
├── main.py                 # FastAPI application entry point
├── flow.py                 # PocketFlow workflow definition
├── nodes.py                # PocketFlow node implementations
├── requirements.txt        # Python dependencies
├── test_chatbot.py        # Test script
├── utils/
│   ├── call_llm.py        # OpenAI API wrapper
│   ├── web_scraper.py     # Web scraping utilities
│   └── url_utils.py       # URL processing utilities
├── static/
│   ├── index.html         # Frontend HTML
│   ├── style.css          # Frontend styling
│   └── script.js          # Frontend JavaScript
└── docs/
    └── design.md          # Technical design documentation
```

## 🎯 Usage Examples

### Example Questions

Try asking these types of questions:

- "What are your return policies?"
- "How do I contact customer support?"
- "What payment methods do you accept?"
- "Do you offer international shipping?"
- "What are your business hours?"

### Example Websites

Good websites to test with:
- Company websites with clear navigation
- E-commerce sites with product/policy pages
- Documentation sites
- Support/help sites

## 🛠️ Development

### Adding New Features

1. **New Utility Functions**: Add to `utils/` directory
2. **New Nodes**: Extend or modify `nodes.py`
3. **Flow Changes**: Update `flow.py`
4. **API Changes**: Modify `main.py`

### Testing

- Run `python test_chatbot.py` for basic validation
- Test individual components in their respective files
- Use the web interface for end-to-end testing

## 🤝 Contributing

This project demonstrates the PocketFlow framework for building intelligent agents. Feel free to:

- Improve the crawling logic
- Enhance the agent decision-making
- Add new utility functions
- Improve the user interface
- Add more robust error handling

## 🐳 Docker Deployment

### Local Docker Testing

```bash
# Build the Docker image
docker build -t website-chatbot .

# Run the container locally
docker run -p 8000:8000 -e PORT=8000 -e OPENAI_API_KEY=your-key website-chatbot
```

### AI Builders Space Deployment

This project is ready for deployment to ai-builders.space platform:

#### Prerequisites
- Public GitHub repository
- All changes committed and pushed to GitHub
- OpenAI API key (or will use provided AI_BUILDER_TOKEN)

#### Deployment Information Required:
1. **GitHub Repository URL**: `https://github.com/username/repo-name`
2. **Service Name**: Unique name for your service (e.g., `website-chatbot`)
3. **Git Branch**: Branch to deploy (e.g., `main`)

#### Deployment Features:
- ✅ Dockerfile optimized for 256MB RAM limit
- ✅ Proper PORT environment variable handling
- ✅ Single process architecture (FastAPI serves both API and static files)
- ✅ Health check endpoints for reliability
- ✅ Security optimized with non-root user
- ✅ Static file serving from single process

The deployed service will be available at: `https://your-service-name.ai-builders.space`

### Production Considerations

- **Memory Limit**: 256MB RAM - keep dependencies lean
- **Port Configuration**: Automatically handled via PORT environment variable
- **API Keys**: AI_BUILDER_TOKEN provided automatically
- **Static Files**: Served efficiently from FastAPI process
- **Health Checks**: Built into Dockerfile for monitoring

## 📄 Original Template

This project was built on the [PocketFlow Project Template](https://github.com/The-Pocket/PocketFlow) for Agentic Coding.

- Learn more about [Agentic Coding Guidance](https://the-pocket.github.io/PocketFlow/guide.html)
- Check out the [YouTube Tutorial](https://www.youtube.com/@ZacharyLLM?sub_confirmation=1)
