# Cognee-Integration-Strands

A powerful integration between Cognee and Strands that provides intelligent knowledge management and retrieval capabilities for AI agents.

> **Note:** This package requires Python 3.10+.

## Overview

`cognee-integration-strands` combines Cognee's advanced knowledge storage and retrieval system with Strands' agent framework. This integration allows you to build AI agents that can efficiently store, search, and retrieve information from a persistent knowledge base using Cognee's graph-based storage.

## Features

- **Smart Knowledge Storage**: Add and persist information using Cognee's advanced indexing.
- **Semantic Search**: Retrieve relevant information using natural language queries.
- **Session Management**: Support for user-specific data isolation using `node_set`.
- **Strands Integration**: Seamless integration with Strands' agent framework.
- **Background Async Support**: Automatically handles Cognee's async operations in a background thread, making it easy to use with Strands tools.

## Installation

```bash
pip install cognee-integration-strands
```

## Quick Start

```python
import os
import asyncio
from cognee_integration_strands import get_sessionized_cognee_tools
from cognee_integration_strands.tools import run_cognee_task
from strands import Agent
from strands.models.openai import OpenAIModel
import cognee

# Configure your OpenAI model
model = OpenAIModel(
    client_args={"api_key": os.getenv("LLM_API_KEY")},
    model_id="gpt-4o",
)

# Get sessionized tools for a specific user
add_tool, search_tool = get_sessionized_cognee_tools("user-123")

# Create an agent with the tools
agent = Agent(
    model=model,
    tools=[add_tool, search_tool]
)

# Use the agent to store information
agent("Remember that we have signed a contract with Meditech Solutions for £1.2M.")

# Use the agent to retrieve information
response = agent("What is the value of the Meditech Solutions contract?")
print(response)
```

## Available Tools

### `get_sessionized_cognee_tools(session_id: Optional[str] = None)`

Returns cognee tools with optional user-specific sessionization.

**Parameters:**

- `session_id` (optional): User identifier for data isolation. If not provided, a random session ID is auto-generated.

**Returns:** `(add_tool, search_tool)` - A list of tools for storing and searching data.

**Usage:**

```python
# With sessionization (recommended for multi-user apps)
add_tool, search_tool = get_sessionized_cognee_tools("user-123")

# Without explicit session (auto-generates session ID)
add_tool, search_tool = get_sessionized_cognee_tools()
```

### Individual Tools

- **`add_tool`**: Stores information in the knowledge base. It handles the asynchronous addition and cognition process in the background.
- **`search_tool`**: Searches and retrieves previously stored information from the knowledge base.

## Session Management

`cognee-integration-strands` supports user-specific sessions to isolate data between different users or contexts. This is achieved by passing a `session_id` to `get_sessionized_cognee_tools`, which ensures that all data stored via `add_tool` is associated with that specific user ID (via Cognee's `node_set` feature).

```python
# User 1 Session
user1_tools = get_sessionized_cognee_tools("user-123")
agent1 = Agent(model=model, tools=user1_tools)

# User 2 Session
user2_tools = get_sessionized_cognee_tools("user-456")
agent2 = Agent(model=model, tools=user2_tools)
```

## Configuration

Copy the `.env.template` file to `.env` and fill out the required API keys:

```bash
cp .env.template .env
```

Then edit the `.env` file and set your API keys:

```env
LLM_API_KEY=your-openai-api-key-here
# Add other configuration as needed
```

## Examples

Check out the `examples/` directory for more comprehensive usage examples:

- `examples/example.py`: Demonstrates setting up Cognee, ingesting data, and using an agent to query that data.
- `examples/session_example.py`: Demonstrates advanced session handling with visualization.

## Requirements

- Python 3.10+
- Cognee
- Strands Agents
- OpenAI API key (for the example model)
