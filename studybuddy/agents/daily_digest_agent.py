# In studybuddy/agents/daily_digest_agent.py (UPDATED TAVILY VERSION)

import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from studybuddy.core.config import settings
# <<< CHANGE 1: Import the new 'search_tool' instead of 'search_and_browse'
from studybuddy.tools.web_tools import search_tool

class AgentState(TypedDict):
    """The state of our agent."""
    messages: Annotated[List[AnyMessage], operator.add]

def create_daily_digest_agent():
    """Creates and compiles the LangGraph agent."""
    
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # We use a powerful model that is good at following instructions
    llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=settings.GROQ_API_KEY)
    
    # <<< CHANGE 2: Give the LLM and the agent our new 'search_tool'
    llm_with_tools = llm.bind_tools([search_tool])
    tools = [search_tool]

    # --- Agent Nodes (Your robust tool-calling logic is perfect and needs no changes) ---
    def call_model(state: AgentState):
        """Invokes the LLM with the current message history."""
        response = llm_with_tools.invoke(state["messages"])
        return {"messages": [response]}

    def call_tool(state: AgentState):
        """Executes any tool calls requested by the LLM."""
        last_message = state["messages"][-1]
        tool_results = []
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            for tool_call in last_message.tool_calls:
                tool_name = tool_call.get("name")
                print(f"--- Attempting to call tool: {tool_name} ---")
                
                tool_found = False
                for tool in tools:
                    # The Tavily tool's name is 'tavily_search_results_json'
                    if tool.name == tool_name:
                        try:
                            result = tool.invoke(tool_call.get("args"))
                            tool_results.append(ToolMessage(content=str(result), tool_call_id=tool_call.get("id")))
                            tool_found = True
                            print(f"--- Successfully called tool: {tool_name} ---")
                        except Exception as e:
                            tool_results.append(ToolMessage(content=f"Error: {e}", tool_call_id=tool_call.get("id")))
                            tool_found = True
                        break
                
                if not tool_found:
                    tool_results.append(ToolMessage(content=f"Tool '{tool_name}' not found.", tool_call_id=tool_call.get("id")))
        
        return {"messages": tool_results}

    # --- Conditional Edge (No changes needed) ---
    def should_continue(state: AgentState):
        """Determines the next step."""
        last_message = state["messages"][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "call_tool"
        else:
            return END

    # --- Build and Compile the Graph (No changes needed) ---
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

    # <<< CHANGE 3: The SystemMessage is no longer needed. The LLM is smart enough
    # to use the Tavily tool based on its description alone.
    
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