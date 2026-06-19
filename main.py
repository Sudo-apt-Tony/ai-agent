"""
Developer: Anthony Smyth
Course: Boot.dev AI Agent Project - Backend Development Learning Path
2026
"""

import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except RuntimeError:
        print(
            f"{RuntimeError}\n Invalid API key. Check .env file for more information."
        )

    client = genai.Client(api_key=api_key)  # pyright: ignore[reportPossiblyUnboundVariable]

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    model = "gemini-2.5-flash"

    try:
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )
        reply = response.text
        usg_md = response.usage_metadata
        function_call = response.function_calls
    except errors.APIError as e:
        print(f"Model is busy or returned an error: {e}")
        return

    if usg_md is None:
        raise RuntimeError(
            f"{RuntimeError}\n Prompt failed. Please check internet connection and validate API key."
        )
    elif args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usg_md.prompt_token_count}")
        print(f"Response tokens: {usg_md.candidates_token_count}")
    function_call_result = []
    if function_call:
        for call in function_call:
            function_call_result.append(call_function(call))

    function_results = []
    for i in function_call_result:
        if not i.parts:
            raise Exception("Function call result does not contain any parts.")
        function_response = i.parts[0].function_response
        if not function_response:
            raise Exception("Function Response object is type None at parts[0].")
        function_response_info = function_response.response
        if not function_response_info:
            raise Exception("Response field None in function response")
        function_results.append(i.parts[0])
        if args.verbose:
            print(f"-> {i.parts[0].function_response.response}")
    print(reply)


if __name__ == "__main__":
    main()
