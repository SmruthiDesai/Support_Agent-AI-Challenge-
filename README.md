# Multi-Agent Customer Care System Demo

A demonstration of coordinated AI agents providing comprehensive customer support using Python 3, FastAPI, OpenAI API, and Google Gemini API.

## 🚀 Quick Start

### 1. Set up Environment
```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies (Python 3.10+ required)
pip install -r requirements.txt
```

### 2. Configure API Keys (Optional)
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note**: The system works without API keys using mock responses for demonstration.

### 3. Start the Server
```bash
python main.py
```

The API will be available at: http://localhost:8000  
Interactive documentation at: http://localhost:8000/docs

## 🧪 Test the System

Run validation tests:
```bash
python test_system.py
```

Test the API endpoints:
```bash
# Run demo scenario
curl -X GET http://localhost:8000/demo

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My laptop order #12345 won'\''t turn on, I need help!"}'

# Check system status
curl -X GET http://localhost:8000/
```

## 🤖 How It Works

### Demo Scenario
Customer: *"My laptop order #12345 won't turn on, I need help!"*

1. **Orchestrator** analyzes request and creates execution plan
2. **Order Agent** retrieves order #12345 details and warranty info
3. **Tech Support Agent** provides troubleshooting steps for power issues
4. **Solutions Agent** offers resolution options (repair/replacement/refund)
5. **Orchestrator** synthesizes all responses into coherent customer service answer

### Multi-Agent Architecture

- **🎯 Orchestrator**: Coordinates all specialist agents and synthesizes responses
- **📦 Order Agent**: Handles order tracking, modifications, returns, warranty
- **🔧 Tech Support Agent**: Provides troubleshooting and technical assistance
- **🛍️ Product Agent**: Offers product information, comparisons, recommendations
- **💡 Solutions Agent**: Manages returns, exchanges, and problem resolution

### Key Features

- ✅ **Works without API keys** (uses intelligent mock responses)
- ✅ **Real-time multi-agent coordination** with parallel/sequential execution
- ✅ **Session-based conversation memory** maintains context
- ✅ **Comprehensive logging** with colored output for demo visibility
- ✅ **30-second timeout protection** prevents hanging requests
- ✅ **Graceful error handling** with fallback strategies
- ✅ **RESTful API** with interactive documentation

## 📁 Project Structure

```
├── main.py                     # FastAPI application entry point
├── agents/                     # All agent implementations
│   ├── orchestrator.py        # Main coordinator
│   ├── order_agent.py         # Order specialist
│   ├── tech_support_agent.py  # Technical support
│   ├── product_agent.py       # Product expert
│   └── solutions_agent.py     # Solutions specialist
├── data/                       # Mock data for demonstration
├── memory/                     # Session and conversation management
├── planning/                   # Agent coordination and planning
├── tools/                      # Tool library for agents
└── utils/                      # Logging and formatting utilities
```

## 🌐 API Endpoints

- `GET /` - Health check and system status
- `POST /chat` - Process customer messages with multi-agent coordination
- `GET /session/{id}` - Retrieve conversation history
- `GET /agents` - List all available agents and capabilities
- `GET /demo` - Run pre-scripted demo scenario
- `POST /reset` - Clear all sessions for demo reset

## 🔧 Troubleshooting

**Dependencies fail to install?**
- Ensure Python 3.10+ is installed
- Try: `pip install --upgrade pip setuptools wheel`

**"Module not found" errors?**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**API timeouts?**
- Check network connection for external API calls
- Adjust timeout in `config.py` if needed

**Port 8000 in use?**
- Change port in `main.py`: `uvicorn.run(..., port=8001)`

## 📊 System Requirements

- **Python**: 3.10 or higher
- **Memory**: 512MB+ RAM
- **Dependencies**: See `requirements.txt`
- **Optional**: OpenAI API key, Google Gemini API key

---

**Demo ready!** 🎭 This system showcases advanced multi-agent coordination, natural language processing, and comprehensive customer service automation.