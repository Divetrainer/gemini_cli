import os
import sys
import argparse
from functions.prompts import system_prompt
from functions.call_function import available_functions, call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

def generate_content(client, messages, verbose):
	model = "gemini-2.5-flash"

	agent_response = client.models.generate_content(
		model = model,
		contents = messages,
		config=types.GenerateContentConfig(
			tools=[available_functions],
				system_instruction=system_prompt,
				temperature=0
			),
		)

	if agent_response.usage_metadata is None:
		raise RuntimeError("API Key error, please check prompt")

	prompt_token = agent_response.usage_metadata.prompt_token_count
	candidate_token = agent_response.usage_metadata.candidates_token_count

	if verbose:
		print("Prompt tokens: ", prompt_token)
		print("Response tokens: ", candidate_token)

	if agent_response.candidates:
		for candidate in agent_response.candidates:
			if candidate.content:
				messages.append(candidate.content)

	if not agent_response.function_calls:
		return agent_response.text

	function_responses = []

	for call in agent_response.function_calls:
		result = call_function(call, verbose)

		if not result.parts:
			raise Exception("Error in processing Function Call")
		if result.parts[0].function_response is None:
			raise Exception("Error")
		if result.parts[0].function_response.response is None:
			raise Exception("Error in processing Function Call")

		function_responses.append(result.parts[0])

		if verbose:
			print(f"-> {result.parts[0].function_response.response}")

	messages.append(types.Content(role="user", parts=function_responses))

def main():
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

	if args.verbose:
		print(f"User prompt: {args.user_prompt}\n")

	for _ in range(20):
		final = generate_content(client, messages, args.verbose)
		if final:
			print("Final response:")
			print(final)
			return
	print("Maximum iterations reached")
	sys.exit(1)



if __name__ == "__main__":
    main()
