# Weather Analysis System

A weather analysis system built with the Model Context Protocol (MCP) that provides AI-powered weather services through multiple client-server architectures.

## Overview

This project implements an MCP-based weather analysis system that combines weather station data with AI-powered analysis capabilities. It supports multiple LLM providers (Anthropic Claude and OpenAI GPT) and offers flexible client-server communication through both STDIO and Server-Sent Events (SSE) transports.

## Architecture

### Components

- **MCP Server**: FastMCP-based server providing weather resources, tools, and prompts
- **Chat Clients**: Multiple client implementations for different transport mechanisms
- **LLM Clients**: Abstract client layer supporting multiple AI providers
- **Weather Data**: Static weather station information and analysis templates

### Key Features

- **Multi-transport Support**: STDIO and SSE communication protocols
- **Multi-LLM Support**: Compatible with Anthropic Claude and OpenAI GPT models
- **Weather Resources**: Access to weather station data and analysis prompts
- **Tool Integration**: Domain suggestion and content generation capabilities
- **Interactive Chat Interface**: Command-line chat interface for weather queries

## Project Structure

```
weather/
├── server/
│   ├── server_script.py    # MCP server implementation
│   └── data.py            # Weather station data and prompts
├── client/
│   ├── client.py          # Base chat client class
│   ├── sse_client.py      # SSE transport client
│   └── stdio_chat_client.py # STDIO transport client
├── llm_clients/
│   ├── client_abc.py      # LLM client abstract base class
│   ├── anthropic_client.py # Anthropic Claude integration
│   └── openai_client.py   # OpenAI GPT integration
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

Once a client is running, you can interact with the weather system:

```
Query: Tell me about weather stations
Query: Analyze the weather for New York
Query: quit
```

## MCP Resources and Tools

### Resources

- `weather://stations`: Weather station data including IDs, names, locations, and coordinates

### Prompts

- `weather_analysis`: Template for comprehensive weather condition analysis

### Tools

- `get_domain_suggestions`: Generate domain name suggestions
- `generate_post_content`: Create post content based on descriptions

## Weather Station Data

The system includes data for major airports:
- John F. Kennedy International Airport (KJFK) - New York, NY
- Los Angeles International Airport (KLAX) - Los Angeles, CA
- O'Hare International Airport (KORD) - Chicago, IL

Each station includes:
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
- National Weather Service API integration ready

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

### Extending Weather Data

Weather station data can be extended in `server/data.py` by adding new entries to the `WEATHER_STATIONS_DATA` dictionary.

## Dependencies

Core dependencies include:
- `httpx`: HTTP client for API requests
- `mcp[cli]`: Model Context Protocol framework
- `anthropic`: Anthropic Claude API client
- `openai`: OpenAI GPT API client
- `requests`: HTTP library for external API calls

## License

[Add license information here]

## Contributing

[Add contribution guidelines here]
