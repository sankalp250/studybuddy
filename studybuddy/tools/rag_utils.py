"""RAG utilities for resume storage and retrieval using vector database.

On small deployments (like Render free tier with 512MB RAM), local embeddings
models (FastEmbed / ONNX / PyTorch) can easily exceed memory limits and trigger
OOM SIGKILL resulting in 502 Bad Gateway errors.
To prevent crashes, RAG vector storage defaults to disabled (ENABLE_RAG=false).
The app seamlessly uses LLM-powered resume summarization and context injection
into the interview agent directly via PostgreSQL.
"""
import os
from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Toggle to disable heavy local vector embeddings on low-memory deployments
ENABLE_RAG = os.getenv("ENABLE_RAG", "false").lower() == "true"

# Global vector store and embeddings (lazy-loaded only when ENABLE_RAG is true)
_vector_store = None
_embeddings = None


def get_embeddings():
    """Get or create the embeddings model (if RAG is enabled)."""
    if not ENABLE_RAG:
        raise RuntimeError("RAG is disabled (ENABLE_RAG is not set to 'true').")

    global _embeddings
    if _embeddings is None:
        from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
        # Use FastEmbed - lightweight and fast, no PyTorch required
        _embeddings = FastEmbedEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            threads=None,
            cache_dir="./chroma_db/fastembed_cache"
        )
    return _embeddings


def get_vector_store(user_id: int, persist_directory: Optional[str] = None):
    """
    Get or create a vector store for a specific user.
    Each user gets their own collection in ChromaDB.
    """
    if not ENABLE_RAG:
        raise RuntimeError("RAG is disabled (ENABLE_RAG is not set to 'true').")

    global _vector_store
    from langchain_community.vectorstores import Chroma
    
    if persist_directory is None:
        persist_directory = os.path.join(os.getcwd(), "chroma_db", f"user_{user_id}")
        os.makedirs(persist_directory, exist_ok=True)
    
    collection_name = f"resume_user_{user_id}"
    embeddings = get_embeddings()
    
    _vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name
    )
    
    return _vector_store


def store_resume(user_id: int, resume_text: str, resume_summary: Optional[str] = None):
    """
    Store resume text in the vector database.
    When RAG is disabled, returns 0 immediately so resume summary is saved
    and interview prep functions cleanly without loading heavy local models.
    """
    if not ENABLE_RAG:
        print("[RAG] store_resume called: RAG vector store disabled to conserve memory. Summary saved in DB.")
        return 0

    try:
        vector_store = get_vector_store(user_id)
        
        # Delete existing resume chunks for this user (to allow re-upload)
        try:
            existing_docs = vector_store.get()
            if existing_docs and existing_docs.get('ids'):
                vector_store.delete(ids=existing_docs['ids'])
        except Exception as e:
            print(f"Note: Could not clear existing resume chunks: {e}")
        
        # Split resume into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        documents = []
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
        
        if documents:
            vector_store.add_documents(documents)
        
        return len(documents)
    except Exception as e:
        print(f"[RAG] Vector storage failed: {e}")
        return 0


def retrieve_relevant_resume_chunks(user_id: int, query: str, k: int = 3) -> List[Document]:
    """Retrieve relevant resume chunks based on a query."""
    if not ENABLE_RAG:
        return []
    try:
        vector_store = get_vector_store(user_id)
        return vector_store.similarity_search(query, k=k)
    except Exception as e:
        print(f"Error retrieving resume chunks: {e}")
        return []


def get_resume_context_for_topic(user_id: int, study_topic: str, k: int = 3) -> str:
    """Get relevant resume context for a study topic."""
    chunks = retrieve_relevant_resume_chunks(user_id, study_topic, k=k)
    if not chunks:
        return ""
    
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        chunk_type = chunk.metadata.get("type", "resume_content")
        context_parts.append(f"[Resume Context {i} - {chunk_type}]:\n{chunk.page_content}")
    
    return "\n\n".join(context_parts)


def delete_user_resume(user_id: int):
    """Delete all resume chunks for a user."""
    if not ENABLE_RAG:
        return True
    try:
        vector_store = get_vector_store(user_id)
        existing_docs = vector_store.get()
        if existing_docs and existing_docs.get('ids'):
            vector_store.delete(ids=existing_docs['ids'])
        return True
    except Exception as e:
        print(f"Error deleting user resume: {e}")
        return False
