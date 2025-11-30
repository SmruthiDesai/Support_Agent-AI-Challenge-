
---

# **Support Agent – AI Challenge (Multi-Agent Customer Care System)**

*A fully functional AI-powered Support Assistant built for Rooman’s 48-Hour AI Agent Development Challenge.*

This project demonstrates a **multi-agent customer care system** that handles real-world support scenarios such as order tracking, product inquiries, technical troubleshooting, and warranty/return assistance.

It is built using **Python, FastAPI, Streamlit, OpenAI/Gemini (optional), and a custom planner + memory system**.

---
## 🔗 Live Demo

Public Streamlit Demo (via ngrok):

👉 https://unequine-roman-downward.ngrok-free.dev

# 🌟 **1. Overview**

This AI Agent acts as a **Customer Support Assistant** that:

* Understands customer queries
* Coordinates multiple specialist agents
* Retrieves product/order information
* Troubleshoots technical issues
* Suggests solutions (returns, replacements, repair)
* Maintains conversation memory
* Generates a unified human-like response

Even **without API keys**, the system works using **mock data** (Orders, Products, Troubleshooting Knowledge Base).

---
## 🧠 **2. Architecture Diagram**

![Architecture Diagram](architecture.png)


# 🧩 **3. Features**

### ✅ Multi-Agent Coordination

* Orchestrator decides which agents to use
* Agents run sequentially or parallel
* Unified response for user

### ✅ Specialist Agents

* **Order Agent:** track, warranty, returns
* **Tech Support Agent:** troubleshooting
* **Product Agent:** comparisons, info
* **Solutions Agent:** next steps & resolution

### ✅ Mock Database

No external APIs needed. Includes:

* Orders
* Products
* Troubleshooting knowledge base
* Company policies

### ✅ Streamlit UI (Demo Interface)

* Real-time agent activity
* Conversation memory
* Execution plan viewer
* Clean chat interface
* Session reset

### ✅ FastAPI Backend

* `/chat` endpoint
* `/agents`, `/session`, `/demo`
* Fully modular

### ✅ Works Without API Keys

* Falls back to mock responses
* No billing required

---

# ⚠️ **4. Limitations**

* External API calls disabled unless real OpenAI/Gemini keys are added
* Order + Product data is mock only
* Troubleshooting uses rule-based knowledge base
* Planner + Synthesis can't use API if quota is exhausted
* No real payment/shipping integration
* Not optimized for large enterprise datasets

---

# 🔧 **5. Tech Stack**

### **Backend**

* Python 3
* FastAPI
* AsyncIO
* Uvicorn

### **Frontend**

* Streamlit

### **AI / NLP**

* Custom LLM planner
* Optional OpenAI GPT-4o
* Optional Gemini Flash

### **Memory**

* Custom session memory
* In-memory storage

### **Data**

* Python mock databases (JSON-like)
* Product/Orders/Troubleshooting

---

# 🚀 **6. Setup Instructions**

### **1. Clone repo**

```bash
git clone https://github.com/SmruthiDesai/Support_Agent-AI-Challenge.git
cd Support_Agent-AI-Challenge
```

### **2. Install dependencies**

```bash
pip install -r requirements.txt
```

### **3. (Optional) Add API Keys**

```
OPENAI_API_KEY=your_key
GEMINI_API_KEY=your_key
```

Without keys → system uses mock responses.

---

# 💻 **7. Running the System**

### Option A — **Streamlit UI (recommended for demo)**

```bash
streamlit run streamlit_app.py
```

Open:
👉 [http://localhost:8501](http://localhost:8501)

### Option B — **FastAPI Backend**

```bash
python main.py
```

API Docs:
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

# 🧪 **8. Testing**

### Run test script

```bash
python test_system.py
```

### Example API call

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My laptop order #12345 won\'t turn on"}'
```

---

# 🎯 **9. Potential Improvements**

* Integrate real databases (Firebase / Supabase)
* Add vector search & embeddings for KB
* Connect to Shopify / Razorpay / real order systems
* Add email/SMS notifications
* Convert to CrewAI multi-agent graph
* Deploy Streamlit on cloud for live demo
* Add agent analytics dashboard
* Add user authentication

---

