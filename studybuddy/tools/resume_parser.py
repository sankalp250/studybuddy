"""Utility functions for parsing and processing resumes."""
import fitz  # PyMuPDF
from io import BytesIO

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text content from a PDF file."""
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in pdf_document:
            text += page.get_text()
        pdf_document.close()
        return text
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")

def extract_text_from_upload(uploaded_file) -> str:
    """Extract text from uploaded file (PDF or text)."""
    file_bytes = uploaded_file.read()
    
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    elif uploaded_file.type == "text/plain":
        return file_bytes.decode('utf-8')
    else:
        raise ValueError(f"Unsupported file type: {uploaded_file.type}")

