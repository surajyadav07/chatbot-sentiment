# Real-Time Chatbot with Sentiment Analysis

A Python-based chatbot using LangGraph that maintains conversation history, analyzes user sentiment (positive, negative, neutral), and responds adaptively. The workflow dynamically routes based on user input and sentiment.

## Features
- Stores message history with timestamps.
- Analyzes sentiment using keyword-based detection.
- Responds adaptively (e.g., encouraging for positive, empathetic for negative).
- Summarizes conversation on command ("summarize").
- Persists state using `MemorySaver`.

## Prerequisites
- Python 3.8+
- Git

## Setup
1. Clone the repository:
   bash
   git clone https://github.com/yourusername/chatbot-sentiment.git
   cd chatbot-sentiment
   
2. Create a virtual environment:
   bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
  
3. Install dependencies:
   bash
   pip install -r requirements.txt
   
4. Run the chatbot:
   bash
   python chatbot_sentiment.py
   

## Usage
- The script includes sample inputs to demonstrate functionality.
- To interact manually:
  1. Modify the `messages` list in `chatbot_sentiment.py` with your input (e.g., `{"role": "user", "content": "I’m happy!", "timestamp": ""}`).
  2. Run the script to process and respond.
  3. Use "summarize" as input to get a conversation summary.
- Example:
  python
  initial_input = {
      "messages": [{"role": "user", "content": "I’m feeling great today!", "timestamp": ""}],
      "sentiment": "neutral"
  }
  

## Project Structure
- chatbot_sentiment.py`: Main script with LangGraph workflow.
- requirements.txt`: Dependencies.
- README.md`: This file.
- .gitignore`: Ignores virtual environment and cache files.

## Contributing
Feel free to open issues or submit pull requests for improvements.
