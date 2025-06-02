# db_utils.py
from sqlalchemy import create_engine, text
import streamlit as st # Used for st.cache_resource, st.sidebar.write
from prompts import ANSWER_PROMPT # Import ANSWER_PROMPT for summarize_answer

# Initialize SQL Engine - using Streamlit's cache_resource
@st.cache_resource
def get_sql_engine():
    return create_engine("sqlite:///data/medical.db")

SQL_ENGINE = get_sql_engine()

def handle_sql_query(llm_model, question, chat_history: list):
    formatted_history = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in chat_history])

    schema = f"""
Tables:
- doctors(full_name TEXT PRIMARY KEY, specialization TEXT, field_of_interest TEXT, institution_name TEXT)
- institutions(name TEXT PRIMARY KEY, type TEXT, address TEXT)
  - The 'type' column for institutions can ONLY be 'Private' or 'Public'.

Conversation History:
{formatted_history}

Instructions for SQL Generation:
- The `full_name` column in 'doctors' and the `name` column in 'institutions' are **text primary keys**, not numerical IDs.
- **CRITICAL RULE FOR ALL STRING MATCHING:** When comparing or matching ANY text field (e.g., `full_name`, `specialization`, `name`, `type`, `address`, `field_of_interest`, `institution_name`), **ALWAYS use the `LIKE` operator with wildcards (`%`) on both sides of the value.**
- **NEVER use the `=` operator for any string comparisons or matching.**
- **Case-Insensitivity Fallback:** To ensure matches regardless of case, **ALWAYS apply the `LOWER()` function to both the database column and the search term.** For example: `WHERE LOWER(full_name) LIKE LOWER('%john doe%')`.
- Analyze the `Conversation History` and the current `Question` to infer context. If the current question is ambiguous (e.g., uses pronouns like "his", "her", "it", "their", or refers to "the doctor" or "the institution"), look back at the history to understand which entity is being referred to.
- Ensure foreign key relationships are correctly handled. For example, to find doctors at an institution, use JOIN on `doctors.institution_name` and `institutions.name`.
- Prioritize retrieving relevant information based on the question.
- **INSTITUTION TYPE MAPPING:** When the user refers to institution types using common terms like 'hospitals', 'clinics', 'ambulances', 'medical centers', 'private hospitals', 'public clinics', etc., understand that these refer to the `institutions.type` column. Remember that the ONLY valid values for 'type' in the database are strictly 'Private' or 'Public'. Map the user's intent to one of these two values.

- **ULTIMATE COLUMN SELECTION RULE:**
  - **FOR EVERY QUERY, ALWAYS select ALL columns FROM ALL TABLES INVOLVED IN THE QUERY.**
  - **Specifically, if a JOIN is used, ensure the SELECT clause effectively covers all columns from both (or more) joined tables.**
  - **Your SELECT clause must be `SELECT *` (or explicitly list all columns from all relevant tables if `SELECT *` is not supported by the specific query structure, though `SELECT *` is generally preferred here).**
  - **NEVER filter or restrict which columns are returned.**
  
- Return ONLY valid SQLite SQL code. Do NOT include any additional words, explanations, markdown formatting (like ```sql), or prefixes (like "SQL:", "sqlite:", "SQL"). The response MUST be just the SQL query itself.
"""
    prompt = f"""Given the following SQL schema, conversation history, and instructions:
{schema}

Translate the user's question to a SQL query:
Question: {question}
SQL Query:"""
    
    response = llm_model.invoke(prompt)
    
    sql_query = response.strip()
    sql_query = sql_query.replace("```", "").replace("sqlite", "").replace("SQL:", "").strip()
    if sql_query.lower().startswith("sql"):
        sql_query = sql_query[3:].strip()
    
    st.sidebar.write(f"Generated SQL query: `{sql_query}`")

    try:
        with SQL_ENGINE.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = result.fetchall()
            columns = result.keys()
            formatted_results = [dict(zip(columns, row)) for row in rows]
            return formatted_results if formatted_results else []
    except Exception as e:
        return f"SQL Error: {e}"

# NOTE: summarize_answer is a core logic function, it will be moved to core_logic.py
# but we need it here to fulfill the import of ANSWER_PROMPT for now
# It will be removed from here later.