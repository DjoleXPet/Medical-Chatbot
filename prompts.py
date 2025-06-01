# prompts.py
from langchain.prompts import PromptTemplate

ROUTING_PROMPT = PromptTemplate.from_template("""
Given the following conversation history and the current user's question, classify the question.

Conversation History:
{chat_history}

Classify this question into one of the following categories:
- SQL: if it's asking about doctors or institutions in the database (e.g., names, specializations, addresses, counts)
- RAG: if it's asking for general medical knowledge that is not directly queryable from the database.
- GENERAL: if it's a general knowledge question not related to medicine or the database.
Return only one word: SQL, RAG, or GENERAL

Question: {question}
""")

GENERAL_ANSWER_PROMPT = PromptTemplate.from_template("""
You are a helpful, concise, and professional general knowledge assistant.
Given the following conversation history and the current user's question, provide a concise answer based on your general knowledge.
Do not provide medical advice or reference any specific databases.
Keep your response brief and to the point, avoiding conversational fillers.

Conversation History:
{chat_history}

Question: {question}

Concise Answer:
""")

ANSWER_PROMPT = PromptTemplate.from_template("""
You are a helpful and concise chatbot assistant.
Given the previous conversation history, the original user's current question, and the data retrieved, provide a short, clear, and natural language answer.
DO NOT add new information or change the core facts from the 'Retrieved Data'.
If the 'Retrieved Data' is empty or indicates an error, state that you couldn't find information.

IMPORTANT RULES:
- **ONLY use the information present in the 'Retrieved Data' to answer the question.**
- DO NOT use any outside knowledge or common sense.
- If the 'Retrieved Data' does not contain enough information to answer the question, clearly state "I couldn't find enough information in my knowledge base to answer that."
- DO NOT invent or make up facts.
- Keep your response brief and to the point, avoiding conversational fillers.
                                             


Conversation History:
{chat_history}

Original Question: {question}
Retrieved Data: {retrieved_data}

Concise Answer:
""")