import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("API Key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()


messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)

contents= args.user_prompt
model="gemini-2.5-flash"


gen_ai_response = client.models.generate_content(
	model = model , contents = messages,
	)

if gen_ai_response.usage_metadata is None:
	raise RuntimeError("API Key error, please check prompt")

prompt_token = gen_ai_response.usage_metadata.prompt_token_count
candidate_token = gen_ai_response.usage_metadata.candidates_token_count

def verbose():
	if args.verbose:
		print(f"User prompt: ", contents)
		print(f"Prompt tokens: ", prompt_token)
		print(f"Response tokens: ", candidate_token)

def main():
	verbose()
	print(gen_ai_response.text)

if __name__ == "__main__":
    main()
