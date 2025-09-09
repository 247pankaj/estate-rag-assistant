# 🏠 EstateRAG Assistant

**EstateRAG** is a GenAI-powered assistant for the real estate domain.  
It enables **intelligent document analysis, contract comparison, and contextual Q&A** across property records such as lease agreements, tenancy contracts, and property documents.

---

## 🚀 Features

- 📑 **Document Analysis** – Upload and process real estate contracts and agreements.  
- 🔍 **Lease Comparison** – Identify differences and similarities across multiple rental agreements.  
- 💬 **Intelligent Q&A** – Ask natural language questions about specific clauses or documents.  
- 🧠 **RAG-powered** – Retrieval Augmented Generation (RAG) pipeline for accurate, context-aware answers.  
- 🛡️ **Enterprise Ready** – Modular architecture, easy integration with APIs, and secure deployment.  

---

## 📄 Reference Documents

- Example rental agreement templates: [UpRent Templates](https://uprent.nl/en-nl/templates/rental-agreements)

---


**⚙️ Setup Instructions**
1. Clone Repository
git clone https://github.com/your-org/estate-rag-assistant.git
cd estate-rag-assistant

2. Create and Activate Conda Environment
conda create -p env python=3.10 -y
conda activate ./env

3. Install Dependencies
# Install from requirements.txt
pip install -r requirements.txt


**▶️ Running the Assistant**

Streamlit App (UI Prototype)
streamlit run app.py

FastAPI Backend (API)
uvicorn api.main:app --reload --port 8000

**📌 Roadmap**

 Multi-lingual document support (Dutch, English, German)
 Role-based access and authentication
 Support for multiple vector DB backends
 Advanced clause similarity detection

**🛡️ License**

This project is licensed under the MIT License.
