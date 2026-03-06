import os
import argparse
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

def main():
    print("Hello from ai-agent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("API Key is None")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


    args = parser.parse_args()    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):

        response = client.models.generate_content(model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], 
        system_instruction=system_prompt),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        usage = response.usage_metadata    

        if usage == None:
            raise RuntimeError("usage is None")

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        
        if response.function_calls:
            function_result_list = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                #print(f"Calling function: {function_call.name}({function_call.args})")
                if not function_call_result.parts:
                    raise Exception("No parts in function call result")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("Function Response is None")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("function response response is None")
                function_result_list.append(function_call_result.parts[0])
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
            messages.append(types.Content(role="user", parts=function_result_list))

        else:
            print(response.text)
            break
    print("20 iterations done, max iterations were reached")


    # print(response.text)

if __name__ == "__main__":
    main()


