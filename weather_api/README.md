# Weather API Tool Example

This example demonstrates how to create a tool that integrates with the OpenWeatherMap API to fetch current weather data for a specified location.

## Overview

The Weather API tool:
- Takes a location parameter (city name)
- Makes an API request to OpenWeatherMap
- Returns formatted weather data

## Files Structure

```
weather_api/
  ├── __init__.py         # Empty file for Python package
  ├── definition.py       # Tool metadata and schema
  ├── tool.py             # Implementation
  └── tool_test.py        # Tests (both mocked and real API tests)
```

## Tool Definition

The `definition.py` file defines the tool's metadata:

- **Name**: `weather_api`
- **Description**: Retrieves weather information for a specified location
- **Parameters**:
  - `location` (required): City name
  - `units` (optional): Temperature units (metric/imperial)
- **Secrets**: `OPENWEATHERMAP_API_KEY`
- **Dependencies**: `requests`, `aiohttp`

## Implementation Details

The tool follows a clean architecture pattern:

1. **Parameter Validation**:
   - Validates required parameters
   - Sets defaults for optional parameters

2. **API Communication**:
   - Uses `aiohttp` for async HTTP requests
   - Proper error handling for API responses
   - URL encoding for location names

3. **Response Formatting**:
   - Processes raw API response
   - Returns user-friendly weather information
   - Includes both formatted data and raw data

## Testing Approach

The tool uses a dual testing approach:

### Mock Testing

- Fast unit tests using mocked API responses
- Tests parameter validation logic
- Tests error handling

### Real API Integration Tests

- Optional tests that make real API calls
- Controlled by environment variables:
  - `TEST_REAL_API=true`
  - `OPENWEATHERMAP_API_KEY=your_key`
- Tests actual data fetching and formatting

## Running the Tool

After registering the tool, it can be used with:

```json
{
  "tool": "weather_api",
  "params": {
    "location": "London",
    "units": "metric"
  }
}
```

## Key Learnings

This example demonstrates:

1. **External API Integration**: Making HTTP requests to third-party services
2. **Error Handling**: Proper handling of API errors and edge cases
3. **Secrets Management**: Securely using API keys
4. **Comprehensive Testing**: Both unit and integration tests
5. **Parameter Validation**: Checking and validating user inputs

## Getting an API Key

To use this tool with the real API, you'll need an OpenWeatherMap API key:

1. Sign up at [OpenWeatherMap](https://openweathermap.org/)
2. Generate an API key in your account dashboard
3. Store it as a secret in your Nexus environment