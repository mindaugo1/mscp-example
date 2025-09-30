start-server:
	uv run -m server.server_script

start-http-server:
	uv run -m server.server_script --http

start-stdio-client:
	uv run -m client.stdio_chat_client

start-sse-client:
	uv run -m client.sse_client

