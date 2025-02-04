#!/usr/bin/env python3

import argparse
import os
import google.generativeai as genai
import subprocess

 # parser takes in input and stores in 
def get_input():
    parser = argparse.ArgumentParser()
    """
    # parser.add_argument("echo", help="echo the string you use")
    # parser.add_argument("square", help="display a square of a given number", type=int)
    # parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")
    args=parser.parse_args()
    # print(args.square**2)
    if args.verbosity:
        print("verbosity turned on")
    """
    parser.add_argument("echo", help="echo the string you use")
    args = parser.parse_args()
    prompt = args.echo
    return prompt


# llm pipeline
def model(prompt):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.0-flash-exp",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    model_input = (
        f"Generate a single-line shell script that runs on macOS for the following prompt: '{prompt}'. "
        "Provide only the shell code. Do not include explanations. "
        "Note: **Do not generate any command that deletes/removes files (rm, rmdir, etc.)**."
    )

    response = chat_session.send_message(model_input)
    # print(response.text)
    return response.text

# preprocess the output
def extract_command(output_text):
    lines = output_text.splitlines()
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None

def handle_output(command):
    dangerous_keywords = ["rm", "sudo", "rmdir", "dd", "mkfs", ":(){ :|: & };:"]
    if any(word in command for word in dangerous_keywords):
        print("Chutiya!!!!. Dangerous command detected. Exiting")
        exit(1)

# execute in terminal
def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=True)
    stdout, stdin = process.communicate()
    print(stdout)

def main():
    prompt = get_input()
    output_text = model(prompt)
    command = extract_command(output_text)

    if command:
        handle_output(command)
        execute_command(command)
    else:
        print("No valid shell command was generated.")

if __name__ == "__main__":
    main()