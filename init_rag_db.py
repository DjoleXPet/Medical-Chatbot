import json
import os
import chromadb

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

CHROMA_PERSIST_DIRECTORY = "./chroma_db"
# LangChain's default collection name when using .from_documents without specifying one
CHROMA_DEFAULT_COLLECTION_NAME = "langchain" 

def load_documents(path):
    """Loads documents from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        raw_docs = json.load(f)
    return [Document(page_content=d["content"], metadata={"title": d["title"]}) for d in raw_docs]

def create_chroma_index(documents):
    """
    Empties the existing Chroma collection and then populates it with new documents.
    The persist directory is kept intact.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Connect to the existing Chroma DB instance
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)

    # Get the specific collection (LangChain's default is 'langchain')
    collection = client.get_or_create_collection(name=CHROMA_DEFAULT_COLLECTION_NAME)

    # Delete all existing embeddings from this collection
    current_count = collection.count()
    if current_count > 0:
        print(f"Clearing {current_count} existing embeddings from collection '{CHROMA_DEFAULT_COLLECTION_NAME}'...")
        
        # Get all existing document IDs
        all_ids = collection.get(include=[])['ids']
        
        if all_ids:
            collection.delete(ids=all_ids)
            print(f"Successfully deleted {len(all_ids)} documents.")
        else:
            print("No IDs found to delete despite collection.count() > 0. This is unexpected.")
    else:
        print(f"Collection '{CHROMA_DEFAULT_COLLECTION_NAME}' is already empty.")

    # Add the new documents to the now-empty collection
    print(f"Adding {len(documents)} new documents to collection '{CHROMA_DEFAULT_COLLECTION_NAME}'...")
    vectordb = Chroma.from_documents(
        documents,
        embedding=embeddings,
        persist_directory=CHROMA_PERSIST_DIRECTORY,
        collection_name=CHROMA_DEFAULT_COLLECTION_NAME 
    )
    
    # Ensure changes are written to disk
    vectordb.persist() 
    print("New documents added and persisted successfully.")

if __name__ == "__main__":
    docs = load_documents("data/rag_docs.json")
    create_chroma_index(docs)

    