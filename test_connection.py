"""Quick test script to verify connectivity to the ChatGPT UI API server."""

import sys
sys.path.insert(0, "client")

from gptuapi import GptClient

API_URL = "http://homeserver:7878"

def main():
    print(f"Testing connection to: {API_URL}")
    client = GptClient(API_URL)
    
    try:
        # Test a simple chat completion
        print("\nSending test message: 'Hello, are you there?'")
        articles, duration = client.chat_completions(["Hello, are you there?"])
        
        print(f"\n✓ Success! Response received in {duration:.2f}s")
        print(f"\nResponse articles ({len(articles)}):")
        for i, article in enumerate(articles, 1):
            print(f"  [{i}] {article}")
            
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
