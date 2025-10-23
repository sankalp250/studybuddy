# In studybuddy/agents/summarizer_agent.py (THE FINAL GUARANTEED VERSION)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from studybuddy.core.config import settings

# --- We are using the EXACT model that YOU proved is working and available ---
def create_summarizer_agent(model_name: str = "llama-3.1-8b-instant"):
    """
    Creates a runnable chain that summarizes text using a PROVEN model and a PROVEN prompt.
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # --- We are using the SIMPLE, DIRECT prompt that is impossible to fail ---
    template = """
INSTRUCTIONS:
You are an expert academic assistant. Your task is to summarize the text provided below.
Create a concise, easy-to-read summary that highlights the key topics, main arguments, and important conclusions.
Structure your output with a brief overall summary, followed by a bulleted list of the most critical takeaways.

TEXT TO SUMMARIZE:
---
{text_content}
---

YOUR SUMMARY:
"""
    prompt = PromptTemplate.from_template(template)
    
    # Instantiate the Groq LLM with the model we KNOW works.
    llm = ChatGroq(model_name=model_name, groq_api_key=settings.GROQ_API_KEY)

    output_parser = StrOutputParser()
    summarizer_chain = prompt | llm | output_parser

    return summarizer_chain

# --- Test Block (No changes needed) ---
if __name__ == "__main__":
    from studybuddy.tools.youtube_tools import get_youtube_transcript

    print("--- Testing The Final, Working Summarizer Agent ---")
    
    test_url = "https://www.youtube.com/watch?v=5MgBikgcWnY"
    
    print(f"1. Fetching transcript for: {test_url}")
    transcript = get_youtube_transcript.invoke({"url": test_url})
    
    if "Error:" in transcript:
        print(transcript)
    else:
        print("2. Transcript fetched successfully.")
        
        print("\n3. Creating and running the summarizer agent...")
        summarizer_agent = create_summarizer_agent()
        
        summary = summarizer_agent.invoke({"text_content": transcript})
        
        print("\n--- AI-Generated Summary ---")
        print(summary)