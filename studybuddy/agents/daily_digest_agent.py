# In studybuddy/agents/daily_digest_agent.py 

import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

from studybuddy.core.config import settings
from studybuddy.tools.web_tools import search_and_browse

class AgentState(TypedDict):
    """The state of our agent."""
    messages: Annotated[List[AnyMessage], operator.add]

def create_daily_digest_agent():
    """Creates and compiles the LangGraph agent."""
    
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    # Use a currently supported Groq model (llama-3.1-70b-versatile)
    llm = ChatGroq(model_name="llama-3.1-8b-instant", groq_api_key=settings.GROQ_API_KEY)
    
    llm_with_tools = llm.bind_tools([search_and_browse])
    tools = [search_and_browse]

    # --- Agent Nodes ---
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
                
                # Find the correct tool
                tool_found = False
                for tool in tools:
                    if tool.name == tool_name:
                        try:
                            result = tool.invoke(tool_call.get("args"))
                            tool_results.append(ToolMessage(content=str(result), tool_call_id=tool_call.get("id")))
                            tool_found = True
                            print(f"--- Successfully called tool: {tool_name} ---")
                        except Exception as e:
                            error_msg = f"Error calling tool {tool_name}: {str(e)}"
                            tool_results.append(ToolMessage(content=error_msg, tool_call_id=tool_call.get("id")))
                            tool_found = True
                            print(f"--- Error calling tool {tool_name}: {e} ---")
                        break
                
                if not tool_found:
                    error_msg = f"Tool '{tool_name}' not found. Available tools: {[tool.name for tool in tools]}"
                    tool_results.append(ToolMessage(content=error_msg, tool_call_id=tool_call.get("id")))
                    print(f"--- Tool not found: {tool_name}. Available: {[tool.name for tool in tools]} ---")
        
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
    print("--- Testing Final Daily Digest Agent with Groq (llama-3.1-8b-instant model) ---")
    
    daily_digest_agent = create_daily_digest_agent()
    
    print("\n--- Agent is compiled. Starting a new stream... ---\n")

    # Add system message to clarify available tools
    system_message = SystemMessage(content="You are a helpful AI assistant. You have access to a web search tool called 'search_and_browse' that can search the web and browse results. Use this tool when you need current information. Always use the exact tool name 'search_and_browse' when making tool calls.")
    
    initial_input = {"messages": [system_message, HumanMessage(content="Summarize the latest news about AI in 1-2 concise sentences.")]}
    
    for event in daily_digest_agent.stream(initial_input, stream_mode="values"):
        last_message = event["messages"][-1]
        print("---AGENT EVENT---")
        
        if hasattr(last_message, 'content') and last_message.content:
            print("Content:", last_message.content)
            
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            print("Tool Calls:", last_message.tool_calls)
        
        if isinstance(last_message, ToolMessage):
             print("Result from Tool (first 200 chars):", last_message.content[:200] + "...")

        print("\n" + "="*50 + "\n")

    print("--- Test finished ---")