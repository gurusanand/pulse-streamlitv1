
import streamlit as st

st.title("🧠 Agentic AI – Multi-Agent Workflow")

st.markdown("""
This app demonstrates a **Multi-Agent AI System** that orchestrates Relationship Manager workflows using an agentic architecture.

### 🤖 Key Frameworks & Concepts:
- **LangChain** – Manages chains of prompts, tools, and memory.
- **LangGraph** – Enables directed graph-based flow among agents (e.g., status checker → reviewer → notifier).
- **ReAct Pattern** – Combines reasoning (thought) and acting (tool use) for each agent node.

---

### 🧩 Agent Types:
- **RM Agent**: Initiates deal creation, tracks updates, captures transaction metadata.
- **Review Agent**: Validates readiness, handles approval and comments.
- **Audit Agent**: Writes logs, updates history, monitors decisions.
- **Notification Agent**: Triggers user-visible updates and messages.

---

### 🔧 Tools Used by Agents:
- **Session Memory** (Streamlit) to simulate shared context
- **Custom Tools** for status tracking, audit logging, and communication

---

### 📈 Flow Simulation:
```mermaid
graph TD
    A[RM Agent] --> B[Review Agent]
    B --> C[Audit Agent]
    C --> D[Notification Agent]
```

Each agent operates autonomously and updates state via shared session, mimicking asynchronous agent behaviors.

This mockup is ready to evolve into a fully functional LangChain + LangGraph prototype.
""")
