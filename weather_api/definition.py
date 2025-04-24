import os

# Path to the tool.py file
tool_file_path = os.path.join(os.path.dirname(__file__), 'tool.py')

# Function to read the content of tool.py
def load_tool_code(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Load the code from tool.py
tool_code = load_tool_code(tool_file_path)

# Define the tool metadata
weather_api_definition = {
    "name": "weather_api",
    "description": "Retrieves weather information for a specified location using OpenWeatherMap API",
    "version": "1.0",
    "author": "Nexus",
    "stage": "stable",
    "parameter_schema": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "City name or location (e.g., 'London', 'New York', 'Tokyo')"
            },
            "units": {
                "type": "string",
                "enum": ["metric", "imperial"],
                "description": "Temperature units (metric for Celsius, imperial for Fahrenheit)",
                "default": "metric"
            }
        },
        "required": ["location"]
    },
    "code": tool_code,
    "dependencies": ["requests", "aiohttp"],
    "secret_names": ["OPENWEATHERMAP_API_KEY"],
    "environment_variables": {},
    "host_functions": []
}