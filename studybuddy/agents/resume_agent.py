"""Agent for summarizing resumes using AI."""
from langchain_groq import ChatGroq
from studybuddy.core.config import settings

def create_resume_agent(model_name: str = "llama-3.1-8b-instant"):
    """Creates a simple agent that generates resume summaries."""
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    llm = ChatGroq(model_name=model_name, temperature=0.7, groq_api_key=settings.GROQ_API_KEY)
    
    def summarize_resume(resume_text: str) -> str:
        prompt = f"""You are an expert at analyzing resumes and extracting key information.

Analyze the following resume and create a concise, structured summary that includes:
- Key skills and technologies
- Notable work experiences and projects
- Education background
- Any relevant achievements or certifications

Resume content:
{resume_text}

Provide a clear, well-structured summary (300-500 words):"""
        
        response = llm.invoke(prompt)
        return response.content
    
    return summarize_resume

if __name__ == "__main__":
    print("Testing Resume Agent...")
    agent = create_resume_agent()
    
    test_resume = """
    John Doe
    Software Engineer
    Email: john@example.com
    
    SKILLS: Python, Machine Learning, TensorFlow, PyTorch, AWS
    
    EXPERIENCE:
    - Senior ML Engineer at TechCorp (2020-2024)
      - Built sentiment analysis models using LSTMs
      - Deployed ML pipelines on AWS
      - Led team of 3 engineers
    
    EDUCATION:
    - MS Computer Science, MIT
    - BS Computer Science, Stanford
    """
    
    result = agent(test_resume)
    print("\nResume Summary:")
    print(result)

