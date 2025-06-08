# Agentic-Email-System-MCP-Servers
An intelligent email assistant built with Agentic AI using LangChain and MCP tools. It autonomously reads, classifies, marks emails as read, and replies to important messages helping you keep your inbox clean and efficient.

The project includes:
- **MCP Server** and **MCP Client** to interface with Gmail APIs asynchronously.
- **LangChain Tools** wrapping MCP client calls for use in AI agents.
- A **Streamlit app (`app.py`)** UI to interact with the agent in a user-friendly way.

## Features

- Read latest emails from Gmail inbox.
- Send emails with subject and body.
- Create Gmail labels.
- Delete emails by ID.
- Create draft emails.
- Get and set Gmail signature.
- Powered by LangChain and OpenAI LLMs.
- Uses Google's Gmail API via OAuth 2.0.

## Getting Started

### Prerequisites

- Python 3.9+
- Google Cloud Console project with Gmail API enabled.
- `credentials.json` file downloaded from Google API Console.
- OpenAI API key.

### Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/gmail-langchain-agent.git
cd gmail-langchain-agent
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Place your Google API credentials.json in the root directory.

4. Run the MCP server (this will start the OAuth flow on the first run):
```bash
python mcp_server.py
```

5. Run the Streamlit app:
```bash
streamlit run app.py
```

6. Use the Streamlit UI to interact with your Gmail via the AI-powered agent.

## File Overview

- **mcp_server.py**: MCP server handling Gmail API calls asynchronously.  
- **mcp_client.py**: MCP client functions to call server tools.  
- **gmail_tools.py**: LangChain tools wrapping MCP client functions.  
- **app.py**: Streamlit app UI for interacting with the agent.  
- **requirements.txt**: Python dependencies.  

## Configuration

- Make sure to update your OpenAI API key in `app.py` or set the environment variable `OPENAI_API_KEY`.  
- The first run of the MCP server opens a browser for Gmail OAuth consent.  

## Usage

Enter natural language queries like:

- "Read 5 latest emails"  
- "Send email to john@example.com with subject Hello and body Hi John"  
- "Create a label named Important"  
- "Set my Gmail signature to Best regards, Mukilan"  

The LangChain agent will route the commands to appropriate Gmail API tools.
