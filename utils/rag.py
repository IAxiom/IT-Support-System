import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Define the persistence directory
PERSIST_DIRECTORY = "./chroma_db"

def get_embeddings():
    """
    Returns GoogleGenerativeAIEmbeddings.
    Requires GOOGLE_API_KEY environment variable.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found. RAG may fail.")
    
    # Fallback to FakeEmbeddings due to API Quota limits (429)
    # return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    from langchain_community.embeddings import FakeEmbeddings
    print("Using FakeEmbeddings due to API quota limits.")
    return FakeEmbeddings(size=768) # 768 for Gemini embedding-001 compatibility if needed, or 1536

def get_vector_store():
    """
    Returns the Chroma vector store.
    """
    embeddings = get_embeddings()
    vector_store = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name="it_support_knowledge"
    )
    return vector_store

def add_documents(documents: list):
    """
    Adds documents to the vector store.
    """
    vector_store = get_vector_store()
    vector_store.add_texts(documents)
    # vector_store.persist() # Chroma 0.4+ persists automatically

def query_knowledge_base(query: str, k: int = 3):
    """
    Queries the knowledge base.
    """
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]

def redact_pii(text: str) -> str:
    """
    Simple PII redaction for demonstration (Emails, SSN-like patterns).
    In production, use a library like Microsoft Presidio.
    """
    import re
    # Redact Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL_REDACTED]', text)
    # Redact Phone Numbers (simple)
    text = re.sub(r'\d{3}-\d{3}-\d{4}', '[PHONE_REDACTED]', text)
    return text
