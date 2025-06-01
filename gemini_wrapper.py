from langchain_google_genai import GoogleGenerativeAI

def get_gemini_model():
    return GoogleGenerativeAI(model="gemini-2.5-flash-preview-04-17", temperature=0.3) # gemini-2.0-flash
