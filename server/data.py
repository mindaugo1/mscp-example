USER_AGENT = "weather-app/1.0"

WEATHER_STATIONS_DATA = {
    "stations": [
        {
            "id": "KJFK",
            "name": "John F. Kennedy International Airport",
            "location": "New York, NY",
            "latitude": 40.6386,
            "longitude": -73.7622,
            "elevation": 13,
            "type": "ASOS",
        },
        {
            "id": "KLAX",
            "name": "Los Angeles International Airport",
            "location": "Los Angeles, CA",
            "latitude": 33.9425,
            "longitude": -118.4081,
            "elevation": 125,
            "type": "ASOS",
        },
        {
            "id": "KORD",
            "name": "O'Hare International Airport",
            "location": "Chicago, IL",
            "latitude": 41.9786,
            "longitude": -87.9048,
            "elevation": 672,
            "type": "ASOS",
        },
    ]
}

WETHEAR_ANALYSIS_PROMPT = """You are a professional meteorologist. Analyze the weather data provided and create a comprehensive weather analysis report.

Structure your analysis as follows:

## Current Conditions Summary
- Temperature and feels-like temperature  
- Sky conditions and visibility
- Wind speed and direction
- Humidity and dew point
- Barometric pressure and trend

## Forecast Analysis  
- Short-term outlook (next 24-48 hours)
- Extended forecast trends (3-7 days)
- Precipitation probability and timing
- Temperature trends and extremes

## Weather Impacts
- Travel conditions
- Outdoor activity recommendations  
- Agriculture/gardening implications
- Energy usage considerations

## Special Considerations
- Any weather warnings or watches
- Unusual weather patterns
- Seasonal context and comparison to normals

Please provide clear, actionable insights based on the weather data."""
