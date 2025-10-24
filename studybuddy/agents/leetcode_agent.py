# In studybuddy/agents/leetcode_agent.py

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

from studybuddy.core.config import settings

def create_leetcode_agent(model_name: str = "llama3-70b-8192"):
    """
    Creates a runnable chain that generates a LeetCode-style problem
    based on a given topic and difficulty, using our stable Groq model.
    """
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    template = """
INSTRUCTIONS:
You are an expert programming problem creator, like the staff at LeetCode.
Your task is to generate one high-quality, original programming problem based on the user-specified topic and difficulty.

The output MUST be in Markdown format and strictly follow this structure:

### **Problem: [Problem Title]**
**Difficulty:** [Difficulty Level]

**Description:**
[A clear and concise description of the problem.]

**Example 1:**
Input: [Example Input]
Output: [Example Output]
Explanation: [Brief explanation]

**Example 2:**
Input: [Example Input]
Output: [Example Output]
Explanation: [Brief explanation]

**Constraints:**
- [List any constraints on the input values.]

<details>
<summary>Click to see the solution in Python</summary>

```python
# Provide a clean, well-commented Python solution here.
# The solution should be correct and efficient.
class Solution:
    def solve(self, input_variable):
        # Your code here
        pass
</details>

TOPIC: {topic}
DIFFICULTY: {difficulty}
YOUR GENERATED PROBLEM:
"""

    prompt = PromptTemplate.from_template(template)

    llm = ChatGroq(model_name=model_name, temperature=0.7, groq_api_key=settings.GROQ_API_KEY)

    output_parser = StrOutputParser()

    leetcode_chain = prompt | llm | output_parser

    return leetcode_chain

if __name__ == "__main__":
    print("--- Testing LeetCode Agent ---")
    
    leetcode_agent = create_leetcode_agent()

    problem_input = {
        "topic": "Arrays and Hashing",
        "difficulty": "Medium"
    }

    print(f"1. Generating a problem for Topic: '{problem_input['topic']}', Difficulty: '{problem_input['difficulty']}'")

    generated_problem = leetcode_agent.invoke(problem_input)

    print("\n--- AI-Generated LeetCode Problem ---")
    print(generated_problem)