# Nexus Tool Development Guide

This guide explains how to create, test, and integrate custom tools for the Nexus platform.

## Tool Architecture

In the Nexus platform, tools are modular components that extend the platform's capabilities. Each tool:

1. **Accepts parameters** from the user
2. **Performs a specific function**
3. **Returns a result**

Tools can:
- Call external APIs
- Process data
- Generate content
- Access platform capabilities via host functions

## Tool Structure

Each tool should be organized in its own directory with the following structure:

```
tools/
  └── your_tool_name/
      ├── __init__.py          # Empty file for Python package
      ├── definition.py        # Tool metadata and schema
      ├── tool.py              # Implementation
      └── tool_test.py         # Tests
```

## Development Process

### 1. Create Tool Directory

```bash
mkdir -p tools/your_tool_name
touch tools/your_tool_name/__init__.py
```

### 2. Define Tool Metadata (definition.py)

The `definition.py` file contains metadata about your tool:

```python
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
your_tool_definition = {
    "name": "your_tool_name",
    "description": "Description of what your tool does",
    "version": "1.0",
    "author": "Your Name",
    "stage": "stable",  # Options: dev, beta, stable
    "parameter_schema": {
        "type": "object",
        "properties": {
            "param1": {
                "type": "string",
                "description": "Description of parameter 1"
            },
            "param2": {
                "type": "number",
                "description": "Description of parameter 2"
            }
            # Add more parameters as needed
        },
        "required": ["param1"]  # List required parameters
    },
    "code": tool_code,
    "dependencies": ["requests"],  # List Python packages your tool depends on
    "secret_names": ["API_KEY"],  # List secret names if your tool requires secrets
    "environment_variables": {},  # Environment variables your tool needs
    "host_functions": ["upload_bytes"]  # Host functions your tool needs access to
}
```

### 3. Implement the Tool (tool.py)

Create a `tool.py` file with your implementation:

```python
import json
import logging
from functions import upload_bytes  # Import host functions if needed
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def main(params, secrets):
    """
    Main function that processes parameters and secrets, then returns a result.
    
    Args:
        params: Dictionary containing the tool parameters
        secrets: Dictionary containing secrets needed by the tool
        
    Returns:
        JSON string with the result
    """
    # Process parameters
    param1 = params.get("param1")
    param2 = params.get("param2")
    
    # Use secrets if needed
    api_key = secrets.get("API_KEY")
    
    # Your tool logic here
    result = {"message": f"Processed {param1} with value {param2}"}
    
    # Return JSON string
    return json.dumps(result)

if __name__ == "__main__":
    import sys
    import json
    
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())
    
    # Call the async main function with parameters and secrets
    result = asyncio.run(main(input_data["params"], input_data["secrets"]))
    
    # Print the result to stdout
    print(result)
```

### 4. Write Tests (tool_test.py)

Create tests for your tool:

```python
import pytest
import asyncio
import json
from tools.your_tool_name.tool import main

@pytest.mark.asyncio
async def test_your_tool():
    params = {
        "param1": "test_value",
        "param2": 123
    }
    secrets = {"API_KEY": "test_key"}
    
    # Call the main function
    result = await main(params, secrets)
    result_data = json.loads(result)
    
    # Assert expected results
    assert "message" in result_data
    assert "test_value" in result_data["message"]
```

### 5. Register Your Tool

Add your tool to the `tools_definition.py` file in the tools root directory:

```python
from .your_tool_name.definition import your_tool_definition
# ... other imports

built_in_tools = [
    # ... existing tools
    your_tool_definition
]
```

## Testing Strategies

### Mock Testing

For quick testing with mock data:

1. Run the specific test file:
   ```bash
   pytest tools/your_tool_name/tool_test.py -v
   ```

2. Or run all tool tests:
   ```bash
   pytest tools/ -v
   ```

### Integration Testing

For testing with actual API calls:

1. Set up your environment variables:
   ```bash
   export TEST_REAL_API=true
   export YOUR_API_KEY=your_api_key_here
   ```

2. Run tests with the real API flag:
   ```bash
   TEST_REAL_API=true pytest tools/your_tool_name/tool_test.py -v
   ```

3. Skip integration tests for regular development:
   ```bash
   pytest tools/your_tool_name/tool_test.py -v -k "not real_api"
   ```

## Best Practices

### Security

1. **Never hardcode credentials** - Use the secrets parameter
2. **Validate all inputs** - Never trust user input
3. **Handle errors gracefully** - Return meaningful error messages

### Performance

1. **Use async operations** for I/O bound tasks
2. **Minimize dependencies** to reduce startup time
3. **Cache results** when appropriate

### Reliability

1. **Add timeout handling** for external API calls
2. **Implement retry logic** for transient failures
3. **Validate responses** from external services

### Maintainability

1. **Document your code** clearly
2. **Write comprehensive tests**
3. **Follow consistent naming conventions**

## Tool Permissions Model

Tools operate within a controlled environment with access to:

- **Parameters**: Passed by the user
- **Secrets**: Stored securely in the platform
- **Host Functions**: Platform capabilities explicitly granted to the tool

This sandbox model ensures tools only have access to the resources they need.

## Example Tools

See example implementations in this repository:
- `weather_api/`: Demonstrates calling an external weather API