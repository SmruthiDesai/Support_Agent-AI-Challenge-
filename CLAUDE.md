# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Multi-Agent Customer Care System** - a demonstration of coordinated AI agents providing comprehensive customer support using Python 3, FastAPI, OpenAI API, and Google Gemini API.

## Environment Setup

### Virtual Environment
The project uses a Python virtual environment located in `venv/`:
- **Activate virtual environment**: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)  
- **Install dependencies**: `pip install -r requirements.txt`

### API Keys Configuration
1. Copy `.env.example` to `.env`
2. Add your API keys:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Python Version
- Requires Python 3.10+
- Currently configured for Python 3.13

## Development Commands

### Running the Application
```bash
# Activate virtual environment first
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
python main.py
```

### Alternative run command
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing the System
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

## Project Architecture

### Multi-Agent System Components

1. **Orchestrator Agent** (`agents/orchestrator.py`)
   - Main coordinator that receives requests and manages specialist agents
   - Creates execution plans and synthesizes responses

2. **Specialist Agents**:
   - **Order Agent** (`agents/order_agent.py`) - Order lookups, tracking, returns
   - **Tech Support Agent** (`agents/tech_support_agent.py`) - Troubleshooting and technical help
   - **Product Agent** (`agents/product_agent.py`) - Product info, comparisons, recommendations  
   - **Solutions Agent** (`agents/solutions_agent.py`) - Returns, exchanges, problem resolution

3. **Supporting Systems**:
   - **Memory System** (`memory/session_memory.py`) - Conversation context and history
   - **Planning Module** (`planning/planner.py`) - Creates and validates execution plans
   - **Tool Library** (`tools/`) - Reusable functions for all agents

### Project Structure
```
├── main.py                     # FastAPI application entry point
├── config.py                   # Configuration and API keys
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── agents/                    # All agent implementations
│   ├── base_agent.py         # Base class for all agents
│   ├── orchestrator.py       # Main coordinator
│   ├── order_agent.py        # Order specialist
│   ├── tech_support_agent.py # Technical support
│   ├── product_agent.py      # Product expert
│   └── solutions_agent.py    # Solutions specialist
├── data/                     # Mock data and sample content
│   └── mock_data.py         # Orders, products, knowledge base
├── memory/                   # Session and conversation management
│   └── session_memory.py    # Memory system implementation
├── planning/                 # Agent coordination and planning
│   └── planner.py           # Plan creation and execution
├── tools/                    # Tool library for agents
│   ├── search_tools.py      # Web search using Gemini
│   ├── order_tools.py       # Order management functions
│   ├── product_tools.py     # Product queries and comparison
│   └── knowledge_tools.py   # Knowledge base and policies
└── utils/                    # Utility modules
    ├── logging_config.py     # Colored logging setup
    └── formatters.py         # Response formatting
```

## API Endpoints

- `GET /` - Health check and system status
- `POST /chat` - Process customer messages with multi-agent coordination
- `GET /session/{id}` - Retrieve conversation history
- `GET /agents` - List all available agents and capabilities
- `GET /demo` - Run pre-scripted demo scenario
- `POST /reset` - Clear all sessions for demo reset
- `GET /sessions` - List active session IDs

**Interactive API Documentation**: http://localhost:8000/docs

## Demo Scenario

The system demonstrates multi-agent collaboration through this scenario:
1. Customer: "My laptop order #12345 won't turn on, I need help!"
2. **Order Agent** retrieves order details and warranty info
3. **Tech Support Agent** provides troubleshooting steps
4. **Solutions Agent** offers resolution options (repair/replace/refund)
5. **Orchestrator** synthesizes all responses into coherent answer

## Key Features

- **Async/await** throughout for performance
- **Colored console logging** for demo visibility  
- **Type hints and docstrings** for code clarity
- **30-second timeout** per request
- **Graceful error handling** with fallbacks
- **Mock data** for demonstration (no database required)
- **Session memory** maintains conversation context

## Development Notes

- The system works with or without API keys (uses mock responses as fallback)
- All agents extend `BaseAgent` for consistent behavior
- Planning module supports sequential, parallel, and conditional execution
- Memory system automatically extracts context from conversations
- Comprehensive logging shows agent decisions and tool usage
- Response synthesis creates natural, unified customer service experience

## Troubleshooting

- **"Module not found"**: Ensure virtual environment is activated and dependencies installed
- **API errors**: Check `.env` file has valid API keys
- **Timeout errors**: Complex requests may need adjustment in `config.py`
- **Port conflicts**: Change port in `main.py` if 8000 is in use