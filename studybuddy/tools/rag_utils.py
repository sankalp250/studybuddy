"""RAG utilities for resume storage and retrieval using vector database.

On small deployments (like Render free tier), full RAG can be too memory-heavy
because it needs to load an embeddings model. To keep the app usable there,
we allow RAG to be disabled via the ENABLE_RAG environment variable.

However, we have optimized this to use FastEmbed, which is much lighter than
the previous PyTorch-based implementation.
"""
import os
from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_core.documents import Document

# Toggle to fully disable RAG on low-memory deployments
ENABLE_RAG = os.getenv("ENABLE_RAG", "true").lower() == "true"

# Global vector store and embeddings (lazy-loaded)
_vector_store: Optional[Chroma] = None
_embeddings: Optional[FastEmbedEmbeddings] = None


def get_embeddings():
    """Get or create the embeddings model (if RAG is enabled)."""
    if not ENABLE_RAG:
        raise RuntimeError("RAG is disabled (ENABLE_RAG is not set to 'true').")

    global _embeddings
    if _embeddings is None:
        # Use FastEmbed - lightweight and fast, no PyTorch required
        _embeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5", # High performance, small size
            threads=None, # Use all available threads
            cache_dir="./chroma_db/fastembed_cache" # Cache models locally
        )
    return _embeddings

def get_vector_store(user_id: int, persist_directory: Optional[str] = None):
    """
    Get or create a vector store for a specific user.
    Each user gets their own collection in ChromaDB.
    """
    global _vector_store
    
    if persist_directory is None:
        # Store vector databases in a local directory
        persist_directory = os.path.join(os.getcwd(), "chroma_db", f"user_{user_id}")
        os.makedirs(persist_directory, exist_ok=True)
    
    # Create a user-specific collection name
    collection_name = f"resume_user_{user_id}"
    
    embeddings = get_embeddings()
    
    # Create or load the vector store
    _vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    return _vector_store

def store_resume(user_id: int, resume_text: str, resume_summary: Optional[str] = None):
    """
    Store resume text in the vector database.
    Splits the resume into chunks and stores them with metadata.

    When RAG is disabled, this becomes a no-op and simply returns 0 so that
    the rest of the app (resume summary, interview agent) keeps working
    without loading heavy models into memory.
    """
    if not ENABLE_RAG:
        # RAG disabled – skip vector store writes
        print("[RAG] store_resume called but RAG is disabled; skipping vector storage.")
        return 0
    # Get the vector store for this user
    vector_store = get_vector_store(user_id)
    
    # Delete existing resume chunks for this user (to allow re-upload)
    try:
        # Get all existing documents
        existing_docs = vector_store.get()
        if existing_docs and existing_docs.get('ids'):
            # Delete all existing documents
            vector_store.delete(ids=existing_docs['ids'])
    except Exception as e:
        # If collection doesn't exist or is empty, that's fine
        print(f"Note: Could not clear existing resume chunks: {e}")
    
    # Split resume into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    # Create documents
    documents = []
    
    # Add the full resume text
    resume_chunks = text_splitter.split_text(resume_text)
    for i, chunk in enumerate(resume_chunks):
        documents.append(Document(
            page_content=chunk,
            metadata={
                "user_id": user_id,
                "chunk_index": i,
                "source": "resume",
                "type": "resume_content"
            }
        ))
    
    # Add the summary as a separate document for better retrieval
    if resume_summary:
        summary_chunks = text_splitter.split_text(resume_summary)
        for i, chunk in enumerate(summary_chunks):
            documents.append(Document(
                page_content=chunk,
                metadata={
                    "user_id": user_id,
                    "chunk_index": i,
                    "source": "resume_summary",
                    "type": "summary"
                }
            ))
    
    # Add documents to vector store
    if documents:
        vector_store.add_documents(documents)
        # Chroma automatically persists, but we can be explicit if needed in older versions
        # vector_store.persist() 
    
    return len(documents)

def retrieve_relevant_resume_chunks(user_id: int, query: str, k: int = 3) -> List[Document]:
    """
    Retrieve relevant resume chunks based on a query.
    This is the RAG retrieval step. When RAG is disabled, returns an empty list.
    """
    if not ENABLE_RAG:
        print("[RAG] Retrieval requested but RAG is disabled; returning no chunks.")
        return []
    vector_store = get_vector_store(user_id)
    
    # Perform similarity search
    try:
        docs = vector_store.similarity_search(query, k=k)
        return docs
    except Exception as e:
        print(f"Error retrieving resume chunks: {e}")
        # Return empty list if retrieval fails
        return []

def get_resume_context_for_topic(user_id: int, study_topic: str, k: int = 3) -> str:
    """
    Get relevant resume context for a study topic.
    Returns a formatted string with relevant resume chunks.
    """
    # Retrieve relevant chunks
    chunks = retrieve_relevant_resume_chunks(user_id, study_topic, k=k)
    
    if not chunks:
        return ""
    
    # Format the context
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        chunk_type = chunk.metadata.get("type", "resume_content")
        context_parts.append(f"[Resume Context {i} - {chunk_type}]:\n{chunk.page_content}")
    
    return "\n\n".join(context_parts)

def delete_user_resume(user_id: int):
    """Delete all resume chunks for a user."""
    try:
        vector_store = get_vector_store(user_id)
        existing_docs = vector_store.get()
        if existing_docs and existing_docs.get('ids'):
            vector_store.delete(ids=existing_docs['ids'])
        return True
    except Exception as e:
        print(f"Error deleting user resume: {e}")
        return False
