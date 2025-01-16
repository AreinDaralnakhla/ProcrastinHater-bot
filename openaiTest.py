import openai
import os

# Ensure your API key is set as an environment variable or hard-code it here
# Example of setting API key as an environment variable:
# export OPENAI_API_KEY="your_openai_api_key"
api_key = os.getenv("OPENAI_API_KEY", "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")

# if not api_key:
#     print("Error: OpenAI API key not found. Please set your API key.")
#     exit(1)

# # Set the OpenAI API key
# openai.api_key = api_key

# Define a function to test the OpenAI ChatCompletion API
def test_openai_chat_completion():
    try:
        # Prompt for user input
        prompt = input("Enter your prompt: ")

        # API call
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Replace with the desired model (e.g., "gpt-4o" or "gpt-3.5-turbo")
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

        # Extract and display the response
        print("Response:", response["choices"][0]["message"]["content"])

    except openai.error.InvalidRequestError as e:
        print(f"Invalid Request Error: {e}")
    except openai.error.AuthenticationError as e:
        print(f"Authentication Error: {e}")
    except openai.error.APIConnectionError as e:
        print(f"API Connection Error: {e}")
    except openai.error.RateLimitError as e:
        print(f"Rate Limit Exceeded: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the script
if __name__ == "__main__":
    print("Starting OpenAI API Test Script...")
    test_openai_chat_completion()
