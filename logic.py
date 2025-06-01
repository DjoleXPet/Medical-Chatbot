# core_logic.py
import streamlit as st # Used for st.sidebar.write
from langchain_core.prompts import PromptTemplate # Use langchain_core for prompts
from prompts import ROUTING_PROMPT, GENERAL_ANSWER_PROMPT, ANSWER_PROMPT

def classify_question(llm_model, question, chat_history: list):
    formatted_history = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in chat_history])
    chain = ROUTING_PROMPT | llm_model
    result = chain.invoke({"question": question, "chat_history": formatted_history})
    return result.strip().upper()

def handle_general_query(llm_model, question, chat_history: list):
    st.sidebar.write(f"Handling GENERAL query directly with LLM.")
    formatted_history = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in chat_history])
    chain = GENERAL_ANSWER_PROMPT | llm_model
    result = chain.invoke({"question": question, "chat_history": formatted_history}) # Pass formatted history
    return result.strip()

def summarize_answer(llm_model, question, raw_result, chat_history: list):
    st.sidebar.write(f"Raw result from internal knowledge base: `{raw_result}`")

    retrieved_data_str = str(raw_result) if raw_result else "No relevant information found."
    formatted_history = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in chat_history])

    chain = ANSWER_PROMPT | llm_model
    result = chain.invoke({"question": question, "retrieved_data": retrieved_data_str, "chat_history": formatted_history})
    return result.strip()