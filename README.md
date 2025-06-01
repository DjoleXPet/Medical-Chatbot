# Medical Chatbot with RAG and SQL Integration

This project implements a medical chatbot leveraging a Retrieval-Augmented Generation (RAG) architecture and a SQL database for structured information queries. It utilizes **Google's `gemini-2.5-flash-preview-04-17` model** for powerful natural language understanding and generation.

---

## ✨ Features

* **Intelligent Query Handling:** The chatbot can answer questions by either retrieving relevant information from a custom knowledge base (RAG) or by querying a structured SQLite database.

* **Google Gemini Integration:** Powered by the `gemini-2.5-flash-preview-04-17` model for advanced conversational AI and query interpretation.

* **Retrieval-Augmented Generation (RAG):** Enhances the LLM's knowledge by providing contextual information from a specialized medical document store (ChromaDB).

* **SQL Database Connectivity:** Translates natural language questions into SQL queries to fetch structured data about doctors and medical institutions.

* **Streamlit User Interface:** Provides an interactive and user-friendly web interface for engaging with the chatbot.

* **Conversational Memory:** Maintains a limited chat history to provide more coherent and context-aware responses.

* **Transparent Internal Flow:** The Streamlit application's sidebar displays the internal workings of the chatbot, such as generated SQL queries and retrieved text from the RAG knowledge base. This allows users to see what information the model is using to formulate its answers.

---

## 🛠️ Setup and Installation

Follow these steps to get your chatbot up and running on your local machine.

### 1. Prerequisites

* **Conda (Anaconda or Miniconda):** This project uses Conda for environment management. If you don't have it, [download and install Conda](https://docs.conda.io/en/latest/miniconda.html).

* **Google Gemini API Key:** You'll need an API key to access the Gemini Pro model.

    * Go to [Google AI Studio](https://aistudio.google.com/).

    * Create an API key and ensure you have access to the `gemini-2.5-flash-preview-04-17` model.

### 2. Initial Setup

#### a. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/DjoleXPet/Medical-Chatbot.git
cd Medical-Chatbot
```

#### b. Create `.env` File
Create a file named `.env` in the root of your project directory (`Medical-Chatbot/`) and add your Google Gemini API key:
```
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```


#### c. Create Conda Environment and Install Dependencies
1. **Create a new Conda environment with Python 3.10:**
```
conda create --name medical_chatbot_env python=3.10
```
2. **Activate the newly created Conda environment:**
```
conda activate medical_chatbot_env
```
3. **Install the required Python packages using `pip`:**
```
pip install -r requirements.txt
```
This command will install all necessary libraries, including LangChain, Streamlit, ChromaDB, and Google API integrations, into your isolated Conda environment.
## 🗄️ Database Initialization
Your chatbot utilizes both a SQL database for structured data and a ChromaDB vector store for its RAG capabilities. You need to initialize both before running the application.
### 1. Initialize SQL Database Schema
This script sets up the necessary tables in your SQLite database (`medical.db`).
```
python init_sql_db.py
```



### 2. Populate SQL Database with Dummy Data
To test the SQL integration with pre-generated sample data (doctors, institutions, etc.), run this script:
```
python dummy_data.py
```



### 3. Initialize RAG Knowledge Base
This script processes the medical documents from `data/rag_docs.json`, converts them into embeddings, and stores them in the ChromaDB vector store.
```
python init_rag_db.py
```



This step might take a few moments depending on the size of your `rag_docs.json` file and your internet connection (as it involves calling embedding models).
## ▶️ Running the Application
Once all setup and database initialization steps are complete, you can launch the Streamlit application.
1. **Ensure your `medical_chatbot_env` Conda environment is active:**
```
conda activate medical_chatbot_env
```



2. **Run the Streamlit application:**
```
streamlit run app.py
```



Your default web browser should automatically open to the Streamlit application (typically at `http://localhost:8501`).
## 🧪 Testing and Verification
A Jupyter notebook, `testing.ipynb`, is provided for manually querying and verifying the functionality of both the SQL database and the RAG knowledge base. This is useful for confirming that your data has been loaded correctly and that the retrieval mechanisms are working as expected.
To use it:
1. **Ensure your `medical_chatbot_env` Conda environment is active.**
2. **Install Jupyter Notebook:**
```
pip install notebook
```


3. **Launch Jupyter Notebook from your project root:**
```
jupyter notebook
```


4. Open `testing.ipynb` in your browser and run the cells.
## 💬 Usage and Capabilities
Interact with the chatbot through the Streamlit interface. The chatbot is designed to handle various types of medical queries:
- **General Medical Knowledge (RAG-powered):** Ask questions about diseases, treatments, medical concepts, etc.
    - Example: "What are the common symptoms of hypertension?"
    - Example: "Explain what an MRI scan is used for."
- **Structured Data Queries (SQL-powered):** Ask questions about doctors, their specializations, and medical institutions.
    - Example: "List all cardiologists."
    - Example: "Find institutions in Belgrade."
    - Example: "How many public hospitals are there?"
- **Combined Queries:** The chatbot intelligently routes your question to the appropriate system (RAG, SQL, or general LLM knowledge) to provide the best possible answer.

Feel free to experiment with different types of questions to explore the full range of its capabilities!
