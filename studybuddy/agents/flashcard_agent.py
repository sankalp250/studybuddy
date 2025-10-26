from langchain_groq import ChatGroq
from studybuddy.core.config import settings

def create_flashcard_agent(model_name: str = "llama-3.1-8b-instant"):
    """Creates a simple agent that generates flashcards from text."""
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    llm = ChatGroq(model_name=model_name, temperature=0.7, groq_api_key=settings.GROQ_API_KEY)
    
    def run_agent(text_content: str):
        prompt = f"""You are an expert at creating educational flashcards.

Extract key facts from the following text and create flashcards as a JSON array.
Each flashcard must have "question" and "answer" fields.

Example format:
[
    {{"question": "What is X?", "answer": "X is Y"}},
    {{"question": "How does Z work?", "answer": "Z works by..."}}
]

Text to analyze:
{text_content}

Generate flashcards as JSON array:"""
        
        response = llm.invoke(prompt)
        return response.content
    
    return run_agent

if __name__ == "__main__":
    print("Testing Flashcard Agent...")
    agent = create_flashcard_agent()
    
    test_text = """
    Neural networks are computing systems inspired by biological neural networks.
    They consist of interconnected nodes (neurons) that process information.
    Deep learning uses neural networks with multiple hidden layers.
    Backpropagation is used to train neural networks by adjusting weights.
    """
    
    result = agent(test_text)
    print("\nGenerated Flashcards:")
    print(result)
