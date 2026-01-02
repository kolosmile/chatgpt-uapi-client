"""Debug script to check the raw response format."""

import sys
sys.path.insert(0, "client")

from gptuapi import GptClient

API_URL = "http://homeserver:7878"


def debug_response():
    """Get a raw response to see the format."""
    print(f"Testing raw response from: {API_URL}")
    client = GptClient(API_URL)
    
    prompt = """Generate a random fictional person with a name, age (as a number), and city. Be creative!

Respond ONLY with valid JSON matching this schema:
{
  "type": "object",
  "properties": {
    "name": {"type": "string"},
    "age": {"type": "integer"},
    "city": {"type": "string"}
  },
  "required": ["name", "age"]
}"""
    
    print(f"\nPrompt:\n{prompt}")
    print("\nSending request...")
    
    articles, duration = client.chat_completions([prompt])
    
    print(f"\n✓ Response received in {duration:.2f}s")
    print(f"\nArticles type: {type(articles)}")
    print(f"Number of articles: {len(articles)}")
    
    for i, article in enumerate(articles):
        print(f"\n--- Article {i} ---")
        print(f"Type: {type(article)}")
        print(f"Content: {article!r}")
        
        if isinstance(article, list):
            print(f"\nList contents:")
            for j, item in enumerate(article):
                print(f"  [{j}] Type: {type(item)}, Value: {item!r}")
    
    return 0


if __name__ == "__main__":
    sys.exit(debug_response())
