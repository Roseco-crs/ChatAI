# 🤖 ChatAI 🤖

[![Owner](https://img.shields.io/badge/Owner-Co2fi--Rodolphe--Segbedji-blue.svg)](https://github.com/roseco-crs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()

## 📖 Project Overview

**ChatAI** is an advanced, full-stack conversational platform engineered to provide precise, context-aware assistance across diverse domains—including software engineering, data science, and creative industries. 

While many AI wrappers offer basic chat functionality, **ChatAI** is built as a robust "agentic" workspace. By integrating **LangChain** for sophisticated orchestration and **open-source LLMs** for deep reasoning, the system goes beyond simple query-response. 

> **Key Innovation:** It features a professional-grade **Session Management System**, allowing users to maintain multiple concurrent workstreams, archive relevant discussions, and switch contexts instantly without losing progress.

---

## 💡 Why ChatAI?

* **🌍 Domain Agnostic:** Feature-rich logic designed to assist with everything from debugging complex Python scripts to drafting technical documentation or analyzing datasets.
* **🏗️ Infrastructure First:** Unlike basic scripts, ChatAI is fully **containerized with Docker**, ensuring that the environment—from memory handling to API orchestration—remains consistent whether running on a local workstation or scaled in the cloud.
* **⚡ Performance Focused:** Specifically optimized for deployment on **Hugging Face Spaces**, utilizing high-speed inference endpoints to deliver real-time, streaming responses that feel natural and fluid.




---

## 🌟 Key Features

* **🧠 Advanced Reasoning:** Powered by state-of-the-art Open Source LLMs for deep contextual understanding.
* **📂 Session Management:** Robust handling of multiple conversations. Users can create, switch between, or delete sessions effortlessly.
* **⛓️ LangChain Integrated:** Uses LangChain for optimized memory management and prompt orchestration.
* **⚡ Real-Time Inference:** Deployed on Hugging Face Spaces using Docker for near-instant response times.
* **🎨 Professional UI:** A clean, white-labeled interface that focuses entirely on the conversation.
* **🔒 Secure & Private:** Built with robust secret management to keep your API keys and data safe.

---

## 🛠️ Technical Stack

* **Orchestration:** [LangChain](https://python.langchain.com/) (LLM Chaining & Memory)
* **Frontend:** [Streamlit](https://streamlit.io/) (Clean, interactive UI)
* **Deployment:** [Docker](https://www.docker.com/) (Containerized for consistency)
* **Hosting:** [Hugging Face Spaces](https://huggingface.co/spaces) (Real-time cloud usage)
* **CI/CD:** GitHub Actions (Auto-sync to Hugging Face)

---

## 🚀 Getting Started

### Quick Test
[ChatAI](https://huggingface.co/spaces/Co2fi-crs/ChatAI)

### Prerequisites
- Docker installed on your machine.
- Groq API Key for your Open Source LLM provider.

### Local Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Roseco-crs/ChatAI.git](https://github.com/Roseco-crs/ChatAI.git)
   cd ChatAI 
   docker build -t app.py .
   docker run --env-file .env -p 8501:7860 --name chatai app.py




