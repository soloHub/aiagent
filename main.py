import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function
from config import MAX_ITERS

def main():
    parser = argparse.ArgumentParser(description="Chat with Gemini API")
    parser.add_argument("user_prompt", type=str, help="The prompt to send to the Gemini API")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for gen_content in range(MAX_ITERS):
        try:
            final_response = generated_content(client, messages, args)
            if final_response:
                print(f"Final response:\n{final_response}")
                return
        except Exception as e:
            print(f"Error in generated_content: {e}")

    print(f"Maximum iterations ({MAX_ITERS}) reached.")
    sys.exit(1)


def generated_content(client, messages, args):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response is missing usage metadata.")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=args.verbose)

        # check if function_call_result part is empty and raise an error if it is
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError(f"Empty Function response for {function_call.name}")

        if args.verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        
        function_responses.append(function_call_result.parts[0])
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()
