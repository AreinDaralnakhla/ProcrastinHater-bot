import openai
import os

api_key = os.getenv("OPENAI_API_KEY", "")

def test_openai_chat_completion():
    try:
        prompt = input("Enter your prompt: ")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
        )

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

if __name__ == "__main__":
    print("Starting OpenAI API Test Script...")
    test_openai_chat_completion()
