# rag_utils.py
import streamlit as st # Used for st.cache_resource, st.sidebar.write
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Define ChromaDB constants
CHROMA_PERSIST_DIRECTORY = "./chroma_db"
CHROMA_DEFAULT_COLLECTION_NAME = "langchain"

# Initialize Vectordb - using Streamlit's cache_resource
@st.cache_resource
def initialize_vectordb():
    vectordb = Chroma(
        persist_directory=CHROMA_PERSIST_DIRECTORY, 
        embedding_function=GoogleGenerativeAIEmbeddings(model="models/embedding-001"), 
        collection_name=CHROMA_DEFAULT_COLLECTION_NAME
    )
    return vectordb

def handle_rag_query(question, chat_history: list):
    context_turns = 3 
    
    contextual_elements = []
    for entry in chat_history[-context_turns:]:
        contextual_elements.append(f"{entry['role'].capitalize()}: {entry['content']}")
    
    contextual_query = "\n".join(contextual_elements) + "\nQuestion: " + question
    
    st.sidebar.write(f"RAG Contextual Query: `{contextual_query}`")

    # Access vectordb from Streamlit's session state (initialized in streamlit_app.py)
    # Ensure st.session_state.vectordb is set where initialize_models is called
    docs = st.session_state.vectordb.similarity_search(contextual_query, k=2) 
    return [d.page_content for d in docs]