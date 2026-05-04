import ollama

def test_ollama():
    print("Testing Ollama connection...")

    try:
        # Check if server is running
        response = ollama.list()
        print(f"Available models: {response}")

        # Test simple generation
        print("Testing simple generation with llama3.2...")
        response = ollama.generate(
            model='llama3.2',
            prompt='Hello, respond with just "OK"',
            options={'temperature': 0.1, 'num_predict': 50}
        )
        print(f"Response: {response['response']}")

        print("✅ Ollama is working correctly!")

    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    test_ollama()
