# In studybuddy/agents/daily_digest_agent.py

from typing import TypedDict, Annotated, List
from langchain_core.messages import AnyMessage, BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI

from studybuddy.core.config import settings
from studybuddy.tools.web_tools import search_and_browse

# --- 1. Define the Agent's State ---
# This is the "memory" of our agent. It's a dictionary that holds information
# that gets passed between nodes.
class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], list]

# --- 2. Initialize the LLM and Tools ---
# Make sure GEMINI_API_KEY is set in your .env file
if not settings.GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

# Initialize the LLM (Gemini in this case)
# We "bind" the tool to the LLM so it knows it has access to it.
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=settings.GEMINI_API_KEY)
llm_with_tools = llm.bind_tools([search_and_browse])

tools = [search_and_browse]

# --- 3. Define the Agent's Nodes (the "actions") ---

# This is our first node. It calls the LLM with the current state of messages.
def call_model(state: AgentState):
    """Invokes the LLM with the current message history."""
    print("---CALLING THE LLM---")
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    # We return a dictionary with the response appended to the message list
    return {"messages": [response]}

# Our second node. It executes the tools that the LLM has requested.
def call_tool(state: AgentState):
    """Checks for tool calls and executes them."""
    print("---CHECKING FOR TOOLS---")
    last_message = state["messages"][-1] # The LLM's response is the last message
    
    # If the last message is a tool call, execute it
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        print("No tool calls found.")
        return {"messages": []} # Return empty if no tool calls

    print(f"Found tool calls: {last_message.tool_calls}")
    tool_results = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call.get("name")
        for tool in tools:
            if tool.name == tool_name:
                # Find the right tool and execute it with the provided arguments
                result = tool.invoke(tool_call.get("args"))
                tool_results.append(
                    ToolMessage(content=str(result), tool_call_id=tool_call.get("id"))
                )
    
    return {"messages": tool_results}

# --- 4. Define the Conditional Edge ---

# This function decides where to go next after the LLM has been called.
def should_continue(state: AgentState):
    """Determines the next step based on the LLM's response."""
    print("---ASSESSING NEXT STEP---")
    last_message = state["messages"][-1]
    
    # If the LLM made a tool call, we should go to the 'call_tool' node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "call_tool"
    # Otherwise, the LLM has given a final answer, so we can end
    else:
        return END

# --- 5. Wire up the graph ---

# Instantiate the graph and associate it with our AgentState
workflow = StateGraph(AgentState)

# Add the nodes to the graph
workflow.add_node("call_model", call_model)
workflow.add_node("call_tool", call_tool)

# Set the entry point of the graph
workflow.set_entry_point("call_model")

# Add the conditional edge. After 'call_model', it will check 'should_continue'
# to decide whether to go to 'call_tool' or to 'END'.
workflow.add_conditional_edges(
    "call_model",
    should_continue,
    {
        "call_tool": "call_tool",
        END: END
    }
)

# Add a regular edge. After 'call_tool' finishes, it will always go back to 'call_model'.
# This creates the agentic loop.
workflow.add_edge("call_tool", "call_model")

# Compile the graph into a runnable agent
daily_digest_agent = workflow.compile()

# You can add a simple test here to see if it runs
if __name__ == "__main__":
    print("Testing Daily Digest Agent...")
    initial_input = {"messages": [HumanMessage(content="Summarize the latest AI news in 3 sentences.")]}
    
    for event in daily_digest_agent.stream(initial_input, stream_mode="values"):
        print("---AGENT EVENT---")
        print(event["messages"][-1])
        print("\n")