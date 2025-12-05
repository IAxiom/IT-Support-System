# 🤖 Multi-Agent IT Support System

A next-generation IT Support Simulator powered by **LangGraph**, **Gemini 2.5**, and **Streamlit**. This system demonstrates an autonomous agentic workflow capable of handling complex IT scenarios, from password resets to ransomware detection.

![App Screenshot](https://raw.githubusercontent.com/IAxiom/IT-Support-System/main/webapp_screenshot.png)
*(Note: You'll need to upload a screenshot to your repo or replace this link)*

## 🌟 Features

### 🧠 Intelligent Agents
-   **Intake Agent**: Uses Sentiment Analysis & Entity Extraction to route requests. Auto-escalates frustrated users.
-   **Workflow Agent**: LLM-driven tool selection to handle dynamic requests (e.g., "I need a mouse" -> `order_peripheral`).
-   **Knowledge Agent**: RAG pipeline (Retrieval Augmented Generation) for policy and "how-to" questions.
-   **Escalation Agent**: "Empathy Engine" that adapts tone based on user sentiment (Apologetic vs. Professional).
-   **Log Analysis Agent**: Detects security threats like Phishing and Ransomware patterns.

### 🚀 Capabilities (The "20 Tasks")
The system supports 20+ real-world IT scenarios, including:
-   **Identity**: MFA Reset, Onboarding, Offboarding, Temp Admin Access.
-   **Hardware**: Laptop Refresh checks, Peripheral Ordering.
-   **Network**: Server Reboots (Prod/Dev aware), Wi-Fi troubleshooting.
-   **Security**: Phishing Analysis, Data Exfiltration detection.

## 🛠️ Tech Stack
-   **Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/)
-   **LLM & Embeddings**: Google Gemini 2.5 Flash Lite
-   **Vector DB**: ChromaDB (Local)
-   **UI**: Streamlit
-   **Language**: Python 3.10+

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/IAxiom/IT-Support-System.git
    cd IT-Support-System
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment**:
    You need a Google Gemini API Key.
    ```bash
    export GOOGLE_API_KEY="your_api_key_here"
    ```

4.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

## 🧪 Testing
The system includes a **Dev Button** in the sidebar to simulate 20+ scenarios instantly.
You can also run the verification suite:
```bash
python main.py
```

## ☁️ Deployment
Hosted on **Streamlit Community Cloud**.
1.  Fork this repo.
2.  Go to [share.streamlit.io](https://share.streamlit.io).
3.  Deploy the app and add your `GOOGLE_API_KEY` in the Secrets management.

---
*Built with ❤️ by the Antigravity Team*
