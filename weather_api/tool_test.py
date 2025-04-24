import pytest
import asyncio
import json
import os
from unittest import mock
from weather_api.tool import main, fetch_weather_data

# Sample response for mocking the API
SAMPLE_WEATHER_RESPONSE = {
    "coord": {"lon": -0.1257, "lat": 51.5085},
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 18.5,
        "feels_like": 17.9,
        "temp_min": 16.8,
        "temp_max": 19.8,
        "pressure": 1025,
        "humidity": 61
    },
    "visibility": 10000,
    "wind": {
        "speed": 2.57,
        "deg": 90
    },
    "clouds": {
        "all": 0
    },
    "dt": 1652870682,
    "sys": {
        "type": 2,
        "id": 2019646,
        "country": "GB",
        "sunrise": 1652847272,
        "sunset": 1652903026
    },
    "timezone": 3600,
    "id": 2643743,
    "name": "London",
    "cod": 200
}

# Mock classes for testing
class MockResponse:
    def __init__(self, status, json_data):
        self.status = status
        self._json_data = json_data
        
    async def json(self):
        return self._json_data
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

class MockClientSession:
    def __init__(self, response):
        self.response = response
        
    def get(self, url):
        return self.response
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.mark.asyncio
async def test_fetch_weather_data_success():
    """Test successful weather data fetch with mocks"""
    # Mock the aiohttp.ClientSession
    mock_response = MockResponse(200, SAMPLE_WEATHER_RESPONSE)
    mock_session = MockClientSession(mock_response)
    
    with mock.patch('aiohttp.ClientSession', return_value=mock_session):
        result = await fetch_weather_data("London", "metric", "test_api_key")
        
    assert result["name"] == "London"
    assert result["sys"]["country"] == "GB"
    assert result["weather"][0]["main"] == "Clear"

@pytest.mark.asyncio
async def test_main_function_success():
    """Test the main function with mocked API response"""
    params = {
        "location": "London",
        "units": "metric"
    }
    secrets = {
        "OPENWEATHERMAP_API_KEY": "test_api_key"
    }
    
    # Mock the fetch_weather_data function
    with mock.patch('weather_api.tool.fetch_weather_data', 
                   return_value=SAMPLE_WEATHER_RESPONSE):
        result = await main(params, secrets)
    
    # Parse the JSON result
    result_data = json.loads(result)
    
    # Verify the result
    assert "location" in result_data
    assert result_data["location"] == "London, GB"
    assert "weather" in result_data
    assert result_data["weather"]["condition"] == "Clear"
    assert "18.5 °C" in result_data["weather"]["temperature"]

@pytest.mark.asyncio
async def test_main_function_missing_location():
    """Test the main function with missing location parameter"""
    params = {
        "units": "metric"
    }
    secrets = {
        "OPENWEATHERMAP_API_KEY": "test_api_key"
    }
    
    result = await main(params, secrets)
    result_data = json.loads(result)
    
    assert "error" in result_data
    assert "Location parameter is required" in result_data["error"]

@pytest.mark.asyncio
async def test_main_function_missing_api_key():
    """Test the main function with missing API key"""
    params = {
        "location": "London",
        "units": "metric"
    }
    secrets = {}
    
    result = await main(params, secrets)
    result_data = json.loads(result)
    
    assert "error" in result_data
    assert "API key is required" in result_data["error"]

# NON-MOCKED TESTS - Will use real API calls
# These tests will be skipped if OPENWEATHERMAP_API_KEY is not available
# or if TEST_REAL_API is not set to "true"

@pytest.mark.skipif(
    os.environ.get("TEST_REAL_API") != "true" or 
    "OPENWEATHERMAP_API_KEY" not in os.environ,
    reason="Skipping real API tests. Set TEST_REAL_API=true and provide OPENWEATHERMAP_API_KEY to run"
)
@pytest.mark.asyncio
async def test_real_api_fetch_weather_data():
    """Test with real API call to OpenWeatherMap"""
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    
    # Test with a known location
    result = await fetch_weather_data("London", "metric", api_key)
    
    # Verify the structure of the response
    assert "name" in result
    assert "main" in result
    assert "weather" in result
    assert "wind" in result
    assert "sys" in result
    
    # Basic sanity checks
    assert result["name"], "City name should be present"
    assert result["sys"]["country"], "Country code should be present"
    assert len(result["weather"]) > 0, "Weather data should be present"

@pytest.mark.skipif(
    os.environ.get("TEST_REAL_API") != "true" or 
    "OPENWEATHERMAP_API_KEY" not in os.environ,
    reason="Skipping real API tests. Set TEST_REAL_API=true and provide OPENWEATHERMAP_API_KEY to run"
)
@pytest.mark.asyncio
async def test_real_api_end_to_end():
    """Test the complete flow with real API call"""
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    
    params = {
        "location": "New York",
        "units": "imperial"  # Use imperial units for variety
    }
    secrets = {
        "OPENWEATHERMAP_API_KEY": api_key
    }
    
    # Make the actual API call
    result = await main(params, secrets)
    result_data = json.loads(result)
    
    # Verify the result structure
    assert "location" in result_data
    assert "weather" in result_data
    assert "raw_data" in result_data
    
    # Check the location
    assert "New York" in result_data["location"]
    
    # Check weather fields
    weather = result_data["weather"]
    assert "condition" in weather
    assert "description" in weather
    assert "temperature" in weather
    assert "°F" in weather["temperature"]  # Should be Fahrenheit
    assert "humidity" in weather
    assert "%" in weather["humidity"]
    
    # Check raw data structure
    assert "name" in result_data["raw_data"]
    assert "weather" in result_data["raw_data"]

@pytest.mark.skipif(
    os.environ.get("TEST_REAL_API") != "true" or 
    "OPENWEATHERMAP_API_KEY" not in os.environ,
    reason="Skipping real API tests. Set TEST_REAL_API=true and provide OPENWEATHERMAP_API_KEY to run"
)
@pytest.mark.asyncio
async def test_real_api_invalid_location():
    """Test with an invalid location"""
    api_key = os.environ.get("OPENWEATHERMAP_API_KEY")
    
    params = {
        "location": "ThisCityDoesNotExist123456789",
        "units": "metric"
    }
    secrets = {
        "OPENWEATHERMAP_API_KEY": api_key
    }

    print(secrets)
    
    # This should return an error
    result = await main(params, secrets)
    result_data = json.loads(result)
    
    assert "error" in result_data
    assert "not found" in result_data["error"].lower()