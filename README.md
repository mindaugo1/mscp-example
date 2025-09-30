# MCP Learning Example

A comprehensive learning example demonstrating the Model Context Protocol (MCP) implementation with multiple client-server architectures. Uses weather data as a sample domain to showcase MCP capabilities.

## Overview

This project is a practical learning example that demonstrates how to build MCP-based applications. It showcases client-server communication patterns, multiple transport protocols, LLM provider integrations, and MCP resource/tool/prompt functionality using weather data as a sample domain.

## Architecture

### Components

- **MCP Server**: FastMCP-based server demonstrating resource, tool, and prompt functionality
- **Chat Clients**: Multiple client implementations showcasing different transport mechanisms
- **LLM Clients**: Abstract client layer demonstrating multi-provider integration patterns
- **Sample Data**: Weather station data used as example domain content

### Key Features

- **Multi-transport Support**: Learn STDIO and SSE communication protocols
- **Multi-LLM Support**: Example integration with Anthropic Claude and OpenAI GPT models
- **MCP Resources**: Demonstrates resource serving with sample weather station data
- **MCP Tools**: Example tool implementations for domain suggestions and content generation
- **MCP Prompts**: Template examples for structured AI interactions
- **Interactive Chat Interface**: Command-line interface demonstrating real-time MCP communication

## Project Structure

```
weather/
├── server/
│   ├── server_script.py    # MCP server implementation example
│   └── data.py            # Sample data and prompts
├── client/
│   ├── client.py          # Base chat client class
│   ├── sse_client.py      # SSE transport client example
│   └── stdio_chat_client.py # STDIO transport client example
├── llm_clients/
│   ├── client_abc.py      # LLM client abstract base class
│   ├── anthropic_client.py # Anthropic Claude integration example
│   └── openai_client.py   # OpenAI GPT integration example
├── pyproject.toml         # Project configuration
├── Makefile              # Build and run commands
└── README.md             # This file
```

## Installation

### Prerequisites

- Python 3.11.5 or higher
- UV package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd weather
```

2. Install dependencies:
```bash
uv sync
```

3. Set up environment variables:
Create a `.env` file with your API keys:
```env
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
X_API_KEY=your_api_key_here
```

## Usage

### Starting the Server

**STDIO Server (default):**
```bash
make start-server
# or
uv run -m server.server_script
```

**HTTP/SSE Server:**
```bash
make start-http-server
# or
uv run -m server.server_script --http
```

### Running Clients

**STDIO Client:**
```bash
make start-stdio-client
# or
uv run -m client.stdio_chat_client
```

**SSE Client:**
```bash
make start-sse-client
# or
uv run -m client.sse_client
```

### Interactive Chat

Once a client is running, you can interact with the MCP system:

```
Query: Tell me about available resources
Query: What tools are available?
Query: Get weather station information
Query: quit
```

## MCP Resources and Tools

This section demonstrates the three main MCP capabilities:

### Resources

- `weather://stations`: Example resource serving weather station data including IDs, names, locations, and coordinates

### Prompts

- `weather_analysis`: Example prompt template for comprehensive weather condition analysis

### Tools

- `get_domain_suggestions`: Example tool to generate domain name suggestions
- `generate_post_content`: Example tool to create post content based on descriptions

## Sample Data

The system includes example weather station data for major airports:
- John F. Kennedy International Airport (KJFK) - New York, NY
- Los Angeles International Airport (KLAX) - Los Angeles, CA
- O'Hare International Airport (KORD) - Chicago, IL

Each station entry demonstrates typical resource data structure:
- Station ID and name
- Geographic location and coordinates
- Elevation and equipment type (ASOS)

## Configuration

### LLM Models

**Anthropic Claude:**
- Default model: `claude-3-5-sonnet-20241022`
- Max tokens: 8000

**OpenAI GPT:**
- Default model: `gpt-4.1`
- Max tokens: 8000

### Server Configuration

- Default port: 8080 (HTTP/SSE mode)
- User agent: `weather-app/1.0`
- Example configuration for external API integration patterns

## Development

### Makefile Commands

- `make start-server`: Start STDIO server
- `make start-http-server`: Start HTTP/SSE server
- `make start-stdio-client`: Start STDIO client
- `make start-sse-client`: Start SSE client

### Adding New LLM Providers

1. Create a new client class inheriting from `LlmClient`
2. Implement required abstract methods:
   - `_call_llm()`
   - `set_available_tools()`
   - `set_call_tool_closure()`

### Extending Sample Data

Sample data can be modified in `server/data.py` by updating the `WEATHER_STATIONS_DATA` dictionary to demonstrate different resource patterns.

## Dependencies

Core dependencies include:
- `httpx`: HTTP client for API requests
- `mcp[cli]`: Model Context Protocol framework
- `anthropic`: Anthropic Claude API client
- `openai`: OpenAI GPT API client
- `requests`: HTTP library for external API calls
