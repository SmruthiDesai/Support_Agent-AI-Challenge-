# Multi-Agent Customer Care System - Complete Replication Prompt

**This is a comprehensive prompt to replicate the entire Multi-Agent Customer Care System from scratch using Claude Code.**

---

## 🎯 **Project Requirements**

Create a **production-ready Multi-Agent Customer Care System** that demonstrates coordinated AI agents providing comprehensive customer support.

### **Core Specifications:**
- **Language**: Python 3.10+ (prefer 3.13)
- **Backend**: FastAPI with async/await patterns
- **Frontend**: Streamlit with beautiful chat interface
- **AI Models**: OpenAI GPT-4 + Google Gemini 2.0-flash
- **Architecture**: 5 coordinated AI agents with orchestrator
- **Execution Modes**: Sequential, Parallel, and Conditional coordination
- **Data**: Mock data (no database) for demonstration
- **Total Expected LOC**: ~2,861 lines across 27+ Python files

## 🏗️ **System Architecture Overview**

### **Multi-Agent Components:**
1. **Orchestrator Agent** - Main coordinator, delegates tasks, synthesizes responses
2. **Order Agent** - Order lookups, tracking, returns, warranty
3. **Technical Support Agent** - Troubleshooting, knowledge base search
4. **Product Expert Agent** - Product comparisons, specifications, inventory
5. **Solutions Specialist Agent** - Returns, exchanges, compensation

### **Supporting Systems:**
- **Memory System** - Session-based conversation context and history
- **Planning Module** - Creates and validates execution plans (sequential/parallel/conditional)
- **Tool Library** - Reusable functions for all agents (search, order, product, knowledge)
- **Mock Data System** - Realistic demonstration data (orders, products, policies)

### **Interfaces:**
- **FastAPI Backend** - REST API with full documentation at `/docs`
- **Streamlit Frontend** - Beautiful chat interface with agent visualization

## 📁 **Required Project Structure**

Create this exact file structure:

```
project_root/
├── main.py                     # FastAPI application entry point
├── config.py                   # Configuration and API keys
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Comprehensive documentation
├── CLAUDE.md                  # Claude Code guidance file
├── demo_questions.md          # Demo scenarios and questions
├── streamlit_app.py           # Streamlit frontend interface
├── start_demo.py              # Interactive launcher script
├── test_system.py             # System validation tests
├── start_backend.sh           # Backend startup script
├── start_streamlit.sh         # Streamlit startup script  
├── stop_backend.sh            # Backend shutdown script
├── stop_streamlit.sh          # Streamlit shutdown script
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Base class for all agents
│   ├── orchestrator.py        # Main coordinator
│   ├── order_agent.py         # Order specialist
│   ├── tech_support_agent.py  # Technical support
│   ├── product_agent.py       # Product expert
│   └── solutions_agent.py     # Solutions specialist
├── data/
│   ├── __init__.py
│   └── mock_data.py          # Orders, products, knowledge base
├── memory/
│   ├── __init__.py
│   └── session_memory.py     # Memory system implementation
├── planning/
│   ├── __init__.py
│   └── planner.py            # Plan creation and execution
├── tools/
│   ├── __init__.py
│   ├── search_tools.py       # Web search using Gemini
│   ├── order_tools.py        # Order management functions
│   ├── product_tools.py      # Product queries and comparison
│   └── knowledge_tools.py    # Knowledge base and policies
└── utils/
    ├── __init__.py
    ├── logging_config.py      # Colored logging setup
    └── formatters.py          # Response formatting
```

## 📋 **Dependencies (requirements.txt)**

```txt
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
openai>=1.0.0
google-generativeai>=0.3.0
pydantic>=2.0.0
aiohttp>=3.8.0
python-dotenv>=1.0.0
colorama>=0.4.0
streamlit>=1.28.0
```

## 🔧 **Configuration System (config.py)**

Create centralized configuration with:
- API key loading from environment variables
- Model configurations for each agent type (OpenAI GPT-4)
- Gemini model: `"gemini-2.0-flash"` (NOT `"gemini-pro"` - deprecated)
- Request timeout: 30 seconds
- Agent-specific settings (temperature, max_tokens)

## 💾 **Mock Data System (data/mock_data.py)**

Create realistic demonstration data:

### **Orders (3 sample orders):**
- Order #12345: TechBook Pro 15, $1299.99, delivered, warranty active
- Order #12346: TechBook Gaming 17, $1599.99, in transit
- Order #12347: TechBook Air 13, $899.99, returned

### **Products (4 laptops):**
- TechBook Pro 15: Business laptop, $1299.99, Intel i7, 16GB RAM
- TechBook Gaming 17: Gaming laptop, $1599.99, RTX 4060, 32GB RAM  
- TechBook Air 13: Ultrabook, $899.99, M2 chip, 8GB RAM
- TechBook Workstation 16: Professional, $2199.99, RTX 4070, 64GB RAM

### **Knowledge Base:**
- Troubleshooting guides (laptop won't turn on, overheating, WiFi issues)
- Company policies (returns, warranty, refunds)
- FAQs and technical solutions

## 🤖 **Agent Implementation Guide**

### **Base Agent Pattern (agents/base_agent.py):**
```python
class BaseAgent(ABC):
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
    
    async def generate_response(self, user_message: str, context: Dict[str, Any], 
                               tools_used: List[str] = None) -> Dict[str, Any]:
        # OpenAI API call with error handling and mock fallback
```

### **Orchestrator Agent (agents/orchestrator.py):**
- Coordinates all specialist agents
- Creates execution plans using planning module
- Synthesizes responses from multiple agents
- Updates session memory
- **CRITICAL**: Must call `memory.get_or_create_session(session_id)` before processing

### **Specialist Agents:**
Each agent has:
- Specific domain expertise and system prompt
- Access to relevant tools from tool library
- Consistent response format
- Error handling and mock fallbacks

## 🧠 **Memory System (memory/session_memory.py)**

Implement session-based memory with:

### **Classes:**
- `Message`: Individual message with metadata
- `Session`: Conversation session with context extraction
- `SessionMemory`: Main memory manager

### **Key Features:**
- Automatic context extraction (orders discussed, products mentioned, issues)
- Conversation history persistence
- Session timeout and cleanup
- Context for agents: recent messages, customer preferences, discussion topics

### **Critical Method:**
```python
def get_or_create_session(self, session_id: Optional[str] = None) -> tuple[str, Session]:
    """Get existing session or create new one - prevents session not found errors"""
```

## 📊 **Planning System (planning/planner.py)**

### **Execution Modes:**
```python
class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"    # One agent after another
    PARALLEL = "parallel"       # Multiple agents simultaneously  
    CONDITIONAL = "conditional" # Agents based on dependencies
```

### **Plan Creation:**
- Analyze user requests to determine required agents
- Create step-by-step execution plans
- Validate plans before execution
- Track execution status and results

## 🛠️ **Tool Library (tools/)**

### **search_tools.py (Gemini-based):**
- Web search using Google Gemini 2.0-flash
- Competitor analysis and deals finder
- Product research and comparisons

### **order_tools.py:**
- Order lookup by ID
- Warranty status checking
- Return initiation and tracking
- Order modification functions

### **product_tools.py:**
- Product information retrieval
- Product comparisons and recommendations
- Inventory checking and pricing
- Specification analysis

### **knowledge_tools.py:**
- Troubleshooting guide generation
- Company policy lookup
- FAQ search and retrieval
- Technical solution recommendations

## 🚀 **FastAPI Backend (main.py)**

### **Required Endpoints:**
- `GET /` - Health check and system status
- `POST /chat` - Process customer messages with multi-agent coordination
- `GET /session/{id}` - Retrieve conversation history
- `GET /agents` - List all available agents and capabilities
- `GET /demo` - Run pre-scripted demo scenario
- `POST /reset` - Clear all sessions for demo reset
- `GET /sessions` - List active session IDs

### **CRITICAL Error Handler Fix:**
```python
from fastapi.responses import JSONResponse

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content=format_error_response("Endpoint not found", "not_found")
    )
```

### **Features:**
- CORS middleware for Streamlit communication
- Request timeout protection (30 seconds)
- Comprehensive error handling
- Automatic OpenAPI documentation

## 🎨 **Streamlit Frontend (streamlit_app.py)**

### **UI Components:**
- Clean chat interface with message history
- Agent badges with colored status indicators
- Real-time agent activity tracking with animations
- Memory context panel (orders, products, issues discussed)
- Execution plan visualizer
- One-click example questions

### **Key Features:**
- Session state management
- Async message processing
- Agent coordination visualization
- Beautiful CSS styling with gradients and animations
- Error handling and user feedback

### **Example Questions Integration:**
Pre-built demo questions organized by category:
- Order Support scenarios
- Product Questions
- Technical Support issues
- Follow-up Questions

## 🎭 **Demo System**

### **Primary Demo Scenario:**
**User Input:** "My laptop order #12345 won't turn on, I need help!"

**Expected Flow:**
1. **Orchestrator** analyzes request and creates conditional execution plan
2. **Order Agent** retrieves order #12345 details and warranty info
3. **Tech Support Agent** provides troubleshooting steps for power issues
4. **Solutions Agent** offers resolution options (repair/replacement/refund)
5. **Orchestrator** synthesizes all responses into coherent customer service answer

### **Demo Questions (demo_questions.md):**
Create comprehensive demo scenarios including:
- Primary multi-agent coordination example
- Follow-up questions that test memory persistence
- Various customer service scenarios
- 5-minute, 10-minute, and 15-minute demo flows

## 🔧 **Service Management Scripts**

### **Bash Scripts (executable):**

**start_backend.sh:**
- Check port availability
- Validate virtual environment and dependencies
- Start FastAPI server with proper error checking

**start_streamlit.sh:**
- Check port availability
- Validate Streamlit installation
- Start frontend with proper configuration

**stop_backend.sh:**
- Kill all backend processes
- Clear port 8000
- Verify shutdown

**stop_streamlit.sh:**
- Kill all Streamlit processes
- Clear port 8501
- Verify shutdown

## 🧪 **Testing & Validation (test_system.py)**

Create system validation that tests:
- API endpoint functionality
- Agent coordination and response quality
- Memory system persistence
- Error handling and recovery
- Performance and timeout handling

## 📚 **Documentation Files**

### **README.md:**
- Quick start guide with setup instructions
- Demo scenarios and usage examples
- API documentation and endpoints
- Troubleshooting guide
- Project architecture overview

### **CLAUDE.md:**
- Comprehensive development guidance
- Bash script usage instructions
- Debugging procedures
- Best practices and conventions
- Performance metrics and limitations

## 🐛 **Critical Bug Fixes to Implement**

### **1. Session Management (CRITICAL):**
In `agents/orchestrator.py`, ensure session exists before processing:
```python
# Ensure session exists and get context
session_id, session = memory.get_or_create_session(session_id)
context = memory.get_context_for_agents(session_id)
```

### **2. FastAPI Error Handlers:**
Return JSONResponse objects, not dictionaries:
```python
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(status_code=404, content=format_error_response(...))
```

### **3. Gemini Model Configuration:**
Use current model name in `config.py`:
```python
GEMINI_MODEL = "gemini-2.0-flash"  # NOT "gemini-pro" (deprecated)
```

## 🎯 **Quality Requirements**

### **Code Quality:**
- Type hints for all functions and methods
- Comprehensive docstrings
- Async/await patterns throughout
- Proper error handling with specific exceptions
- Clean separation of concerns

### **User Experience:**
- Beautiful, responsive Streamlit interface
- Clear agent coordination visualization
- Comprehensive error messages
- Fast response times (when using mock data)
- Intuitive demo flow

### **Production Readiness:**
- Environment variable configuration
- Graceful API key handling (works without keys using mocks)
- Proper logging with colored output
- Resource cleanup and timeout protection
- Session management and memory efficiency

## 🚀 **Implementation Strategy**

### **Phase 1: Core Infrastructure**
1. Set up project structure and dependencies
2. Implement configuration system and mock data
3. Create base agent class and memory system
4. Build planning module with execution modes

### **Phase 2: Agent Development**
1. Implement orchestrator with session management fix
2. Create all specialist agents with proper prompts
3. Build comprehensive tool library
4. Test agent coordination and response synthesis

### **Phase 3: Interfaces**
1. Develop FastAPI backend with all endpoints
2. Implement error handlers correctly (JSONResponse)
3. Create Streamlit frontend with agent visualization
4. Build service management scripts

### **Phase 4: Testing & Polish**
1. Comprehensive system testing
2. Demo scenario validation
3. Documentation completion
4. Performance optimization

## 🔍 **Validation Checklist**

After implementation, verify:
- [ ] All 27+ files created with proper structure
- [ ] Both FastAPI (8000) and Streamlit (8501) start without errors
- [ ] Demo scenario executes successfully in ~20-30 seconds
- [ ] Agent coordination shows all three execution modes
- [ ] Memory persists across conversation turns
- [ ] Error handlers return proper JSON responses
- [ ] Bash scripts work for service management
- [ ] API keys are validated (test with/without keys)
- [ ] Comprehensive logging shows agent decisions
- [ ] Beautiful Streamlit UI with agent visualization

## 🎉 **Success Criteria**

The system is complete when:
1. **Demo works end-to-end**: "My laptop order #12345 won't turn on, I need help!" produces coordinated multi-agent response
2. **Beautiful interfaces**: Both FastAPI docs and Streamlit chat are professional and functional
3. **Real AI integration**: OpenAI GPT-4 and Gemini 2.0-flash work with proper fallbacks
4. **Production quality**: Proper error handling, logging, configuration, and documentation
5. **Easy management**: Bash scripts allow simple service start/stop operations

---

**This prompt contains everything needed to replicate the exact Multi-Agent Customer Care System. Follow the specifications precisely to achieve the same functionality, architecture, and user experience.**