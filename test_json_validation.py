"""Test script for JSON validation feature."""

import sys
sys.path.insert(0, "client")

from gptuapi import GptClient, JsonValidationError

API_URL = "http://homeserver:7878"


def test_json_mode():
    """Test JSON mode with schema validation."""
    print(f"Testing JSON validation with: {API_URL}")
    client = GptClient(API_URL)
    
    # Define a simple schema
    person_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "city": {"type": "string"}
        },
        "required": ["name", "age"]
    }
    
    prompt = "Generate a random fictional person with a name, age (as a number), and city. Be creative!"
    
    print(f"\nPrompt: {prompt}")
    print(f"Schema: {person_schema}")
    print("\nSending request (with up to 3 retries if needed)...")
    
    try:
        result, duration = client.chat_completions(
            prompts=[prompt],
            response_schema=person_schema,
            max_retries=3,
            strict=True
        )
        
        print(f"\n✓ Success! Response received in {duration:.2f}s")
        print(f"\nValidated JSON result:")
        print(f"  Name: {result.get('name')}")
        print(f"  Age: {result.get('age')}")
        print(f"  City: {result.get('city', 'N/A')}")
        print(f"\nFull result: {result}")
        return 0
        
    except JsonValidationError as e:
        print(f"\n✗ Validation failed after {e.attempts} attempts")
        print(f"Last errors: {e.errors}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(test_json_mode())
