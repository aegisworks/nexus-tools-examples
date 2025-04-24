# Nexus Tool Development Examples

A comprehensive guide and reference implementations for developing custom tools for the Nexus AI platform.

## Overview

This repository provides practical examples and best practices for creating tools that extend the Nexus platform. It's designed to help developers understand the tool development workflow and implement their own custom tools.

## Repository Structure

```
.
├── README.md                  # General tool development guide
├── weather_api/               # Weather API tool example
│   ├── README.md              # Specific documentation for this example
│   ├── __init__.py
│   ├── definition.py          # Tool metadata & schema
│   ├── tool.py                # Implementation
│   └── tool_test.py           # Tests (both mocked and real)
├── requirements.txt           # Dependencies for all examples
└── future_examples/           # Additional examples (to be added)
```

## Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/aegisworks/nexus-tools-examples.git
   cd nexus-tools-examples
   ```

2. Explore the example implementations in the respective directories

## Examples

### Weather API Tool

A complete example that demonstrates:
- Calling external APIs (OpenWeatherMap)
- Parameter validation and error handling
- Async HTTP requests with aiohttp
- Response formatting and processing
- Comprehensive testing (both mocked and real API)

See the [Weather API README](weather_api/README.md) for detailed documentation.

To run the tests:

```bash
# Run with mocks only
pytest weather_api/tool_test.py -v

# Run with real API (requires API key)
export TEST_REAL_API=true
export OPENWEATHERMAP_API_KEY=your_api_key_here
pytest weather_api/tool_test.py -v
```

## Creating Your Own Tools

The [TOOL_GUIDE.md](TOOL_GUIDE.md) provides comprehensive documentation on:
- Tool architecture and structure
- Creating tool metadata
- Implementing tool logic
- Writing tests
- Security best practices
- Performance optimization
