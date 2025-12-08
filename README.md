# 🤖 IT Support Genius

### Multi-Agent AI System for Enterprise IT Support

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://it-support-system-ybbkyebdj4tskyywnnnhl2.streamlit.app/)

---

## 🎯 Overview

IT Support Genius is a **multi-agent AI system** that automates IT support operations. Built with **LangGraph + Gemini + Jira**, it demonstrates enterprise-grade AI orchestration.

### Key Metrics
| Metric | Value |
|--------|-------|
| **Automation Rate** | 80% |
| **Response Time** | 2.3s avg |
| **Test Pass Rate** | 100% |
| **User Satisfaction** | 85.7% |

---

## 🏗️ Architecture

```
                    ┌─────────────────┐
                    │   USER REQUEST  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  🎯 INTAKE      │
                    │  Intent + Mood  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│ 📚 KNOWLEDGE  │   │ ⚙️ WORKFLOW     │   │ 🚨 ESCALATE │
│   35 IT docs  │   │  11 MCP tools   │   │ Jira + Slack│
└───────────────┘   └─────────────────┘   └─────────────┘
```

---

## 🤖 Agents

| Agent | Purpose | Key Features |
|-------|---------|--------------|
| **Intake** | Request classification | Sentiment, VIP detection, urgency |
| **Knowledge** | Information retrieval | 8-category inline knowledge base |
| **Workflow** | Automation execution | 11 tools, human approval |
| **Escalation** | Human handoff | Real Jira tickets, Slack simulation |
| **Log Analysis** | Security detection | 4 threat patterns |

---

## 🔧 Features

### Core
- ✅ **Multi-Agent Orchestration** - LangGraph state machine
- ✅ **Knowledge Base** - Inline KB with 35 IT docs
- ✅ **Workflow Automation** - 11 MCP tools
- ✅ **Jira Integration** - Real ticket creation
- ✅ **MCP Server** - Standardized tool access

### Advanced
- ✅ **Human-in-the-Loop** - Approval for sensitive actions
- ✅ **Audit Logging** - Full action history
- ✅ **User Role Switching** - VIP/Dev/Regular personas
- ✅ **Confidence Scores** - AI certainty indicators
- ✅ **Security Detection** - Ransomware, phishing, intrusion

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [USE_CASES.md](docs/USE_CASES.md) | 7 IT support scenarios with metrics |
| [PRODUCT_SPEC.md](docs/PRODUCT_SPEC.md) | Problem space, personas, architecture |
| [COMPETITIVE_ANALYSIS.md](docs/COMPETITIVE_ANALYSIS.md) | vs Glean, ServiceNow, Moveworks |
| [UX_DESIGN.md](docs/UX_DESIGN.md) | Wireframes, user flows, design decisions |
| [TESTING.md](docs/TESTING.md) | 31 test cases, 100% passing |
| [DEMO_PRESENTATION.md](docs/DEMO_PRESENTATION.md) | Slides outline + demo script |

---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/IAxiom/IT-Support-System.git
cd IT-Support-System
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Secrets
```bash
export GOOGLE_API_KEY="your-gemini-key"
export JIRA_DOMAIN="your-domain.atlassian.net"
export JIRA_EMAIL="your-email"
export JIRA_API_TOKEN="your-token"
```

### 3. Run
```bash
streamlit run app.py
```

---

## 🧪 Testing

```bash
# Run test scenarios
python test_creative.py

# Test main workflow
python main.py

# Test Jira integration
python integrations/jira_client.py

# Test MCP demo
python mcp_client_demo.py
```

---

## 🎬 Demo

### Live App
🌐 **https://it-support-system-ybbkyebdj4tskyywnnnhl2.streamlit.app/**

### Try These Scenarios
1. "What is the password policy?" → Knowledge Agent
2. "Reset my MFA please" → Workflow Agent
3. "I'm furious, nothing works!" → Escalation (Jira ticket)
4. "Check my system logs" → Log Analysis

---

## 📊 Rubric Compliance

| Requirement | Status |
|-------------|--------|
| Define Use Case | ✅ 7 use cases documented |
| Identify Agents | ✅ 5 agents implemented |
| UX Design | ✅ Wireframes + flows |
| System Development | ✅ LangGraph + Streamlit |
| Testing & Validation | ✅ 31 tests, 100% pass |
| Presentation | ✅ Demo slides + script |
| RAG Integration | ✅ Inline KB (fallback) |
| Workflow Automation | ✅ 11 MCP tools |
| MCP Integration | ✅ Server + client demo |
| Multi-Agent | ✅ LangGraph orchestration |
| Industry Awareness | ✅ Competitive analysis |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Orchestration | LangGraph |
| LLM | Google Gemini 2.5 Flash Lite |
| UI | Streamlit |
| Knowledge Base | Inline (ChromaDB optional) |
| Ticketing | Jira Cloud REST API |
| Standards | Model Context Protocol (MCP) |

---

## 📁 Project Structure

```
it_support_system/
├── agents/                 # 5 AI agents
├── docs/                   # 6 documentation files
├── integrations/           # Jira client
├── tools/                  # MCP tools
├── utils/                  # LLM, RAG utilities
├── app.py                  # Streamlit UI
├── main.py                 # LangGraph workflow
├── mcp_server.py           # MCP server
└── mcp_client_demo.py      # MCP client
```

---

## 👥 Team

- **David Lucas** - Product Owner & Developer

---

*Last Updated: December 2024*
