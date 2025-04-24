import json
import logging
import asyncio
import aiohttp
from urllib.parse import quote

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Base URL for OpenWeatherMap API
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def fetch_weather_data(location, units, api_key):
    """
    Fetch weather data from OpenWeatherMap API
    
    Args:
        location: City name or location
        units: 'metric' or 'imperial'
        api_key: OpenWeatherMap API key
        
    Returns:
        Dictionary with weather data
    """
    # URL encode the location
    encoded_location = quote(location)
    
    # Construct the API URL
    url = f"{API_BASE_URL}?q={encoded_location}&units={units}&appid={api_key}"

    print (f"Fetching weather data from: {url}")
    
    logger.info(f"Fetching weather data for {location}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                elif response.status == 401:
                    logger.error("Invalid API key")
                    raise ValueError("Invalid API key. Please check your API key and try again.")
                elif response.status == 404:
                    logger.error(f"Location '{location}' not found")
                    raise ValueError(f"Location '{location}' not found. Please check the spelling and try again.")
                else:
                    logger.error(f"API error: {response.status}")
                    raise ValueError(f"Failed to fetch weather data: HTTP {response.status}")
    except aiohttp.ClientError as e:
        logger.error(f"HTTP request error: {str(e)}")
        raise ValueError(f"Failed to connect to weather service: {str(e)}")

def format_weather_data(weather_data, units):
    """Format the raw weather data into a more user-friendly structure"""
    
    # Extract and format the data
    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    main_weather = weather_data["weather"][0]["main"]
    description = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    
    city_name = weather_data["name"]
    country = weather_data["sys"]["country"]
    location = f"{city_name}, {country}"
    
    # Format sunrise and sunset times
    sunrise = weather_data["sys"]["sunrise"]
    sunset = weather_data["sys"]["sunset"]
    
    # Format the data
    formatted_data = {
        "location": location,
        "weather": {
            "condition": main_weather,
            "description": description,
            "temperature": f"{temp} {temp_unit}",
            "feels_like": f"{feels_like} {temp_unit}",
            "humidity": f"{humidity}%",
            "wind_speed": f"{wind_speed} {speed_unit}"
        },
        "raw_data": weather_data  # Include raw data for advanced usage
    }
    
    return formatted_data

async def main(params, secrets):
    """
    Main function that processes parameters and fetches weather data.
    
    Args:
        params: Dictionary containing the tool parameters (location, units)
        secrets: Dictionary containing the API key
        
    Returns:
        JSON string with the weather data
    """
    try:
        # Extract parameters
        location = params.get("location")
        if not location:
            return json.dumps({"error": "Location parameter is required"})
        
        units = params.get("units", "metric")
        if units not in ["metric", "imperial"]:
            units = "metric"  # Default to metric if invalid
        
        # Get API key from secrets
        api_key = secrets.get("OPENWEATHERMAP_API_KEY")
        if not api_key:
            return json.dumps({"error": "OpenWeatherMap API key is required"})
        
        # Fetch weather data
        weather_data = await fetch_weather_data(location, units, api_key)
        
        # Format the data
        formatted_data = format_weather_data(weather_data, units)
        
        # Return formatted data as JSON
        return json.dumps(formatted_data)
    
    except ValueError as e:
        # Return error message
        error_response = {
            "error": str(e)
        }
        return json.dumps(error_response)
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        error_response = {
            "error": f"An unexpected error occurred: {str(e)}"
        }
        return json.dumps(error_response)

if __name__ == "__main__":
    import sys
    
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    
    # Call the async main function with parameters and secrets
    result = asyncio.run(main(input_data["params"], input_data["secrets"]))
    
    # Print the result to stdout
    print(result)