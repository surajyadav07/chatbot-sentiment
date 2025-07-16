from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal, List, Dict
from typing_extensions import TypedDict
from datetime import datetime

# Initialize MemorySaver
memory = MemorySaver()

# Define state schema
class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str
    timestamp: str

class ChatState(TypedDict):
    messages: List[Message]
    sentiment: Literal["positive", "negative", "neutral"]

# Node to process user message and analyze sentiment
def process_message(state: ChatState) -> ChatState:
    user_message = state["messages"][-1]["content"].lower()
    positive_keywords = ["great", "happy", "awesome", "good"]
    negative_keywords = ["sad", "bad", "terrible", "angry"]
    
    sentiment = "neutral"
    if any(keyword in user_message for keyword in positive_keywords):
        sentiment = "positive"
    elif any(keyword in user_message for keyword in negative_keywords):
        sentiment = "negative"
    
    state["messages"][-1]["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    state["sentiment"] = sentiment
    return state

# Node to generate adaptive response based on sentiment
def generate_response(state: ChatState) -> ChatState:
    sentiment = state["sentiment"]
    user_message = state["messages"][-1]["content"]
    
    if sentiment == "positive":
        response = f"That’s awesome to hear! 😊 What’s making you feel so {user_message.lower()}?"
    elif sentiment == "negative":
        response = f"I’m sorry you’re feeling that way. 😔 Want to share more about {user_message.lower()}?"
    else:
        response = f"Got it! Tell me more about {user_message}."
    
    state["messages"].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return state

# Node to summarize conversation
def summarize_conversation(state: ChatState) -> ChatState:
    summary = "Conversation Summary:\n"
    for msg in state["messages"]:
        role = "User" if msg["role"] == "user" else "Assistant"
        summary += f"{role} ({msg['timestamp']}): {msg['content']}\n"
    state["messages"].append({
        "role": "assistant",
        "content": summary,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    return state

# Conditional routing function
def route_message(state: ChatState) -> str:
    last_message = state["messages"][-1]["content"].lower()
    if last_message == "summarize":
        return "summarize_conversation"
    return "generate_response"

# Build the graph
builder = StateGraph(ChatState)
builder.add_node("process_message", process_message)
builder.add_node("generate_response", generate_response)
builder.add_node("summarize_conversation", summarize_conversation)

# Define edges
builder.add_edge(START, "process_message")
builder.add_conditional_edges(
    "process_message",
    route_message,
    {
        "generate_response": "generate_response",
        "summarize_conversation": "summarize_conversation"
    }
)
builder.add_edge("generate_response", END)
builder.add_edge("summarize_conversation", END)

# Compile the graph with MemorySaver
graph = builder.compile(checkpointer=memory, interrupt_before=["generate_response"])

# Display the graph
display(Image(graph.get_graph().draw_mermaid_png()))

# Sample usage
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    initial_input = {
        "messages": [{"role": "user", "content": "I’m feeling great today!", "timestamp": ""}],
        "sentiment": "neutral"
    }
    graph.invoke(initial_input, config)

    # Follow-up input
    followup_input = {
        "messages": [
            {"role": "user", "content": "I’m feeling great today!", "timestamp": "2025-07-16 23:25:00"},
            {"role": "assistant", "content": "That’s awesome to hear! 😊 What’s making you feel so great?", "timestamp": "2025-07-16 23:25:01"},
            {"role": "user", "content": "summarize", "timestamp": ""}
        ],
        "sentiment": "neutral"
    }
    graph.invoke(followup_input, config)
```