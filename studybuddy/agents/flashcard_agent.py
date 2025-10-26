# In studybuddy/agents/flashcard_agent.py (THE FINAL, WORKING-MODEL VERSION)

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

from studybuddy.core.config import settings

# --- WE ARE USING THE MODEL THAT IS GUARANTEED TO WORK ---
def create_flashcard_agent(model_name: str = "llama-3.1-8b-instant"):
    """
    Creates a runnable chain that extracts question-answer pairs
    from a given text and formats them as a JSON object using a WORKING model.
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # This is the corrected prompt with escaped curly braces.
    template = """
INSTRUCTIONS:
You are an expert data extraction bot. Your task is to analyze the provided text content
and extract key concepts that can be turned into flashcards.

Read the text and identify distinct question-and-answer pairs.
For each pair, create a JSON object with a "question" key and an "answer" key.

You MUST format your entire output as a single JSON array of these objects, like this:
[
    {{
        "question": "This is the first question.",
        "answer": "This is the corresponding answer."
    }},
    {{
        "question": "This is the second question.",
        "answer": "This is its answer."
    }}
]

Do not include any other text, explanations, or markdown formatting. Your response must be ONLY the JSON array.

TEXT TO ANALYZE:
---
{text_content}
---

YOUR JSON OUTPUT:
"""

    prompt = PromptTemplate.from_template(template)
    
    # Use the working model and bind the JSON response format
    llm = ChatGroq(
        model_name=model_name, 
        temperature=0.1,
        groq_api_key=settings.GROQ_API_KEY
    ).bind(response_format={"type": "json_object"})

    output_parser = JsonOutputParser()
    
    flashcard_chain = prompt | llm | output_parser

    return flashcard_chain

# --- Test Block ---
if __name__ == "__main__":
    import json
    
    print("--- Testing Final Flashcard Generation Agent ---")
    
    flashcard_agent = create_flashcard_agent()
    
    test_conversation = """
    User: What's the difference between supervised and unsupervised learning?
    Assistant: Supervised learning uses labeled data to train a model, where you know the desired output. Examples include classification and regression. Unsupervised learning, on the other hand, works with unlabeled data to find hidden patterns or structures, like in clustering or dimensionality reduction.
    """
    
    print("1. Generating flashcards from sample text...")
    
    try:
        generated_flashcards = flashcard_agent.invoke({"text_content": test_conversation})
        
        print("\n--- AI-Generated Flashcards (as Python objects) ---")
        print(json.dumps(generated_flashcards, indent=2))

    except Exception as e:
        print(f"\n--- An error occurred during agent invocation ---")
        print(e)