import json
import os
from mcp.server.fastmcp import FastMCP

from server.data import WEATHER_STATIONS_DATA, WETHEAR_ANALYSIS_PROMPT
import requests
import dotenv

dotenv.load_dotenv()

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

API_HEADERS = {
    "Content-Type": "application/json",
    "X-API-Key": os.getenv("X_API_KEY"),
}


mcp = FastMCP("weather", port=8080)


@mcp.resource("weather://stations")
def get_weather_stations() -> str:
    """Get information about weather monitoring stations.

    Returns JSON data containing weather station details including IDs, names,
    locations, coordinates, and types of monitoring equipment.
    """
    return json.dumps(WEATHER_STATIONS_DATA, indent=2)


@mcp.prompt("weather_analysis")
def weather_analysis_prompt() -> str:
    """Template for analyzing current weather conditions and forecasts."""
    return WETHEAR_ANALYSIS_PROMPT


@mcp.tool()
async def get_domain_suggestions(description: str, number_of_suggestions: int) -> str:
    """Get domain suggestions given a description of the domain.
    Args:
        description: A description of the domain
        number_of_suggestions: The number of suggestions to return
    """
    url = "http://localhost/domains/generator"
    data = {"description": description, "number_of_suggestions": number_of_suggestions}
    request = requests.post(url, json=data, headers=API_HEADERS)
    domains = " ".join(request.json().get("generated", []))
    return domains or "Problem querying the domain suggestions tool"


@mcp.tool()
async def generate_post_content(description: str) -> str:
    """Generate post content given a description of the post.
    Args:
        description: A description of the post

    """
    url = "http://localhost/wp-plugin"
    data = {
        "description": description,
    }
    request = requests.post(url, json=data, headers=API_HEADERS)
    post_content = request.json()[0].get("content", "")
    with open("/Users/mindaugas.krasauskas/weather/post_contents_1.txt", "w+") as f:
        f.write(post_content)
    return post_content or "This is a post content"


if __name__ == "__main__":
    import sys

    transport = "stdio"
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        transport = "http"

    if transport == "http":
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
