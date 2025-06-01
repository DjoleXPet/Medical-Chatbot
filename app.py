# streamlit_app.py
import streamlit as st
import os
from dotenv import load_dotenv

# --- Streamlit Page Configuration (MUST be the first Streamlit command) ---
st.set_page_config(page_title="Medical Chatbot", page_icon="⚕️")

# Import functions/constants from your new modules
from gemini_wrapper import get_gemini_model # Your LLM wrapper
from sql_utils import handle_sql_query #, get_sql_engine, SQL_ENGINE
from rag_utils import handle_rag_query, initialize_vectordb
from logic import classify_question, handle_general_query, summarize_answer

history_limit = 6

# --- Environment Variables ---
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY") 

# --- Streamlit UI ---
st.title("⚕️ Medical Chatbot")
st.write("Ask me anything about doctors, institutions, or general medical knowledge!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "Hello! How can I help you today?"})

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Cache LLM initialization
@st.cache_resource
def get_llm_model():
    return get_gemini_model()

# Initialize models and store in session_state for access across modules if needed
# get_sql_engine() is called within db_utils.py's global scope, so no need here.
st.session_state.llm = get_llm_model()
st.session_state.vectordb = initialize_vectordb()


# Get user input
if prompt := st.chat_input("What's your question?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    chat_history_for_llm = [
        {"role": m["role"], "content": m["content"]} 
        for m in st.session_state.messages 
        if m["content"] != "Hello! How can I help you today?" 
    ]

    # Limit chat history for less use of tokens
    # if len(chat_history_for_llm) > history_limit:
    #     chat_history_for_llm = chat_history_for_llm[:history_limit]

    with st.spinner("Thinking..."):
        mode = classify_question(st.session_state.llm, prompt, chat_history_for_llm)
        st.info(f"🧭 Routing to: **{mode}**") 

        final_answer = None
        if mode == "SQL":
            raw_result = handle_sql_query(st.session_state.llm, prompt, chat_history_for_llm) 
            final_answer = summarize_answer(st.session_state.llm, prompt, raw_result, chat_history_for_llm)

        elif mode == "RAG":
            raw_result = handle_rag_query(prompt, chat_history_for_llm) # vectordb accessed via st.session_state inside handle_rag_query
            final_answer = summarize_answer(st.session_state.llm, prompt, raw_result, chat_history_for_llm)
        elif mode == "GENERAL":
            final_answer = handle_general_query(st.session_state.llm, prompt, chat_history_for_llm) 
        else:
            final_answer = "I'm sorry, I couldn't understand how to route your question. Please try rephrasing."

    st.session_state.messages.append({"role": "assistant", "content": final_answer})
    with st.chat_message("assistant"):
        st.markdown(final_answer)