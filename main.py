import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

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
    generated_content(client, messages, args)

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

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=args.verbose)

            # check if function_call_result part is empty and raise an error if it is
            if not function_call_result.parts:
                raise Exception("Function call response is missing parts.")
            
            if function_call_result.parts[0].function_response is None:
                raise Exception("Function call response is missing function_response.")

            function_results = []
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            #print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Response: \n{response.text}")

if __name__ == "__main__":
    main()
