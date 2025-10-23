# In studybuddy/agents/summarizer_agent.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from studybuddy.core.config import settings

def create_summarizer_agent(model_name: str = "llama3-70b-8192"):
    """
    Creates a runnable chain that summarizes a given text (e.g., a transcript).
    This is a simple, non-cyclical agent (an LCEL chain).
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # 1. The Prompt Template
    # This is the instruction set for our agent. It tells the LLM its persona
    # and what to do with the {transcript} variable we will provide.
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert academic assistant. Your task is to summarize the provided text. "
            "Create a concise, easy-to-read summary that highlights the key topics, main arguments, and important conclusions. "
            "Structure the output with a brief overall summary, followed by a bulleted list of the most critical takeaways."
        )),
        ("human", "Please summarize the following content:\n\n---\n\n{text_content}")
    ])

    # 2. The LLM
    # The language model that will perform the summarization.
    llm = ChatGroq(model_name=model_name, groq_api_key=settings.GROQ_API_KEY)

    # 3. The Output Parser
    # Ensures the final output from the LLM is a clean string.
    output_parser = StrOutputParser()

    # 4. The Chain
    # We chain these components together using the pipe operator (|).
    # This means the output of the prompt flows into the llm, and its output flows into the parser.
    summarizer_chain = prompt_template | llm | output_parser

    return summarizer_chain


# --- Optional Test Block ---
# This allows us to test the summarizer agent directly.
if __name__ == "__main__":
    from studybuddy.tools.youtube_tools import get_youtube_transcript

    print("--- Testing Summarizer Agent ---")
    
    # Example video: a short lecture on neural networks
    test_url = "https://www.youtube.com/watch?v=aircAruvnKk"
    
    print(f"1. Fetching transcript for: {test_url}")
    transcript = get_youtube_transcript(url=test_url)
    
    if "Error:" in transcript:
        print(transcript)
    else:
        print("2. Transcript fetched successfully (first 200 chars):")
        print(transcript[:200] + "...")
        
        print("\n3. Creating and running the summarizer agent...")
        summarizer_agent = create_summarizer_agent()
        
        # We invoke the agent by passing a dictionary with the key matching the prompt variable
        summary = summarizer_agent.invoke({"text_content": transcript})
        
        print("\n--- AI-Generated Summary ---")
        print(summary)