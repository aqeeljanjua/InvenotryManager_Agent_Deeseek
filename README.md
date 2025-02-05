# Offline AI Agent with Ollama & DeepSeek

An offline-capable AI agent that leverages DeepSeek and Llama2 models through Ollama for natural language processing and intelligent inventory management, with MongoDB integration for data persistence.

## Overview
This project demonstrates an intelligent system that can:
- Process natural language queries offline using local LLM models
- Manage inventory data through MongoDB
- Handle complex business logic without internet connectivity
- Maintain conversation context and chat history
- Generate dynamic database queries from natural language input

## Key Components
- **Ollama Integration**: Local model management and inference
- **DeepSeek Model**: Primary language model for query processing
- **MongoDB Backend**: Persistent data storage and retrieval
- **Query Processing**: Natural language to database query conversion
- **Session Management**: Maintains context across conversations

## Developer
Muhammad Aqeel Yasin  
Shadow Analytics

## Features
- Natural language query processing using Deepseek and Llama2 models
- MongoDB integration for data persistence
- Intelligent query parsing and response generation
- Real-time inventory tracking
- Supplier management
- Chat history tracking
- Session-based interactions

## Prerequisites
- Python 3.8+
- MongoDB
- Ollama

## Installation

1. Clone the repository
```bash
git clone [repository-url]
```

2. Install required packages
```bash
pip install -r requirements.txt
```

3. Install and start MongoDB

4. Install Ollama and pull required models
```bash
ollama pull deepseek-r1:14b
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Enter natural language queries, for example:
- "What is the current stock level of laptops?"
- "Who is the supplier for item ID 1?"
- "Update stock level for laptops"

## Project Structure
- `main.py` - Application entry point
- `query_agent.py` - Main query processing agent
- `database_setup.py` - MongoDB database initialization and operations
- `ollama_helper.py` - LLM integration helper
- `prompt_manager.py` - Manages system prompts
- `query_generator.py` - Generates database queries from natural language


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.