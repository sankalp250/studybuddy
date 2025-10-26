"""Agent for interview preparation without external tools."""
from langchain_groq import ChatGroq
from studybuddy.core.config import settings

def create_interview_agent(model_name: str = "llama-3.1-8b-instant"):
    """Creates a simple interview preparation agent without external tools."""
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    llm = ChatGroq(model_name=model_name, temperature=0.7, groq_api_key=settings.GROQ_API_KEY)
    
    def prepare_interview(messages, resume_context=""):
        """Prepares interview questions and responses based on conversation history."""
        # Convert messages to a single prompt
        conversation_text = ""
        for msg in messages:
            if hasattr(msg, 'content'):
                role = getattr(msg, 'role', 'user') if hasattr(msg, 'role') else 'user'
                conversation_text += f"{role}: {msg.content}\n"
        
        prompt = f"""You are an expert AI interview preparation assistant. Your role is to help users prepare for interviews by:

1. Asking relevant, personalized questions based on their background and resume
2. Providing detailed, helpful answers to their questions
3. Offering constructive feedback and suggestions
4. Generating practice interview questions tailored to their experience

IMPORTANT RULES:
- NEVER use external search tools or function calls
- Provide direct, comprehensive answers based on your knowledge
- Reference specific details from the user's resume when available
- Be conversational and supportive
- Focus on practical interview preparation

{resume_context}

Conversation so far:
{conversation_text}

Respond as a helpful interview preparation coach:"""
        
        response = llm.invoke(prompt)
        return response.content
    
    return prepare_interview

if __name__ == "__main__":
    print("Testing Interview Agent...")
    agent = create_interview_agent()
    
    test_messages = [
        {"role": "user", "content": "I'm preparing for a data science internship interview. Can you ask me some questions?"}
    ]
    
    result = agent(test_messages)
    print("\nInterview Agent Response:")
    print(result)
