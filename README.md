# ChatAI 
---
title: ChatAI
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# 🤖 ChatAI 🤖

[![Owner](https://img.shields.io/badge/Owner-Co2fi--crs-blue.svg)](https://github.com/roseco-crs)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()
[![Sync to HF](https://github.com/roseco-crs/ChatAI/actions/workflows/sync_to_hf.yml/badge.svg)](https://github.com/roseco-crs/ChatAI/actions)

**ChatAI** is a high-performance conversational assistant designed to provide expert-level help across any field. Built with a focus on speed, user experience, and sophisticated conversation logic, ChatAI bridges the gap between complex Large Language Models and intuitive user interactions.



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

### Prerequisites
- Docker installed on your machine.
- An API Key for your Open Source LLM provider (e.g., Groq or Hugging Face).

### Local Installation
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Roseco-crs/ChatAI.git](https://github.com/Roseco-crs/ChatAI.git)
   cd ChatAI 
   docker build -t app.py .
   docker run --env-file .env -p 8501:7860 --name chatai app.py

### Quick Test
[ChatAI](https://huggingface.co/spaces/Co2fi-crs/ChatAI)

