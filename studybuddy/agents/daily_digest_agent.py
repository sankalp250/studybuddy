# In studybuddy/agents/daily_digest_agent.py (UPDATED TAVILY VERSION)

import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from studybuddy.core.config import settings
from studybuddy.tools.web_tools import search_tool

class AgentState(TypedDict):
    """The state of our agent."""
    messages: Annotated[List[AnyMessage], operator.add]

def create_daily_digest_agent(model_name: str = "llama3-70b-8192"): # Add model_name parameter with a default
    """Creates and compiles the LangGraph agent."""
    
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # Use the model_name passed to the function
    llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=settings.GROQ_API_KEY)
    
    llm_with_tools = llm.bind_tools([search_tool])
    tools = [search_tool]


    # --- Agent Nodes ---
    def call_model(state: AgentState):
        """Invokes the LLM with the current message history."""
        messages = list(state["messages"])
        
        # Add system message to force correct tool usage
        system_prompt = (
            "You are a helpful AI assistant. "
            "You have access to a search tool called 'tavily_search'. "
            "ALWAYS use 'tavily_search' to search the web. "
            "Do NOT use 'brave_search' or any other tool name."
        )
        
        # Check if system message already exists
        if not isinstance(messages[0], SystemMessage):
            messages.insert(0, SystemMessage(content=system_prompt))
            
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def call_tool(state: AgentState):
        """Executes any tool calls requested by the LLM."""
        last_message = state["messages"][-1]
        tool_results = []
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                        break
                
                if not tool_found:
                    # Fallback: if model tries to call 'brave_search', try to use Tavily instead if args match
                    if tool_name == 'brave_search':
                        print(f"--- Redirecting 'brave_search' call to 'tavily_search' ---")
                        try:
                            # Tavily expects 'query' arg, brave_search usually uses 'q' or 'query'
                            args = tool_call.get("args")
                            query = args.get('query') or args.get('q')
                            if query:
                                result = search_tool.invoke({"query": query})
                                tool_results.append(ToolMessage(content=str(result), tool_call_id=tool_call.get("id")))
                                tool_found = True
                                print(f"--- Successfully redirected and called Tavily ---")
                        except Exception as e:
                            print(f"--- Redirect failed: {e} ---")

                if not tool_found:
                    tool_results.append(ToolMessage(content=f"Tool '{tool_name}' not found. Please use 'tavily_search'.", tool_call_id=tool_call.get("id")))
        
        return {"messages": tool_results}

    # --- Conditional Edge ---
    def should_continue(state: AgentState):
        """Determines the next step."""
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "call_tool"
        else:
            return END

    # --- Build and Compile the Graph ---
    workflow = StateGraph(AgentState)
    workflow.add_node("call_model", call_model)
    workflow.add_node("call_tool", call_tool)
    workflow.set_entry_point("call_model")
    workflow.add_conditional_edges("call_model", should_continue, {"call_tool": "call_tool", END: END})
    workflow.add_edge("call_tool", "call_model")
    
    return workflow.compile()

# --- Main Test Block ---
if __name__ == "__main__":
    print("--- Testing Final Daily Digest Agent with Tavily Search ---")
    
    daily_digest_agent = create_daily_digest_agent()
    
    print("\n--- Agent is compiled. Starting a new stream... ---\n")
    
    initial_input = {"messages": [HumanMessage(content="What is the latest news about AI? Summarize the top 2-3 stories in a few sentences each.")]}
    
    for event in daily_digest_agent.stream(initial_input, stream_mode="values"):
        last_message = event["messages"][-1]
        print("---AGENT EVENT---")
        
        if hasattr(last_message, 'content') and last_message.content:
            print("Content:", last_message.content)
            
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            print("Tool Calls:", last_message.tool_calls)
        
        if isinstance(last_message, ToolMessage):
             print("Result from Tavily (first 200 chars):", last_message.content[:200] + "...")

        print("\n" + "="*50 + "\n")

    print("--- Test finished ---")