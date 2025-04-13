import json
import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tool: Run shell command
def run_command(command):
    result = os.system(command)
    return f"Executed: {command}"

# Tool: Get weather info (for demo purposes)
def get_weather(city: str):
    url = f"https://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return f"The weather in {city} is {response.text}."
    return "Something went wrong"

# Tool: Write a file to disk
def write_file(input_data):
    try:
        data = json.loads(input_data) if isinstance(input_data, str) else input_data
        file_path = data["file_path"]
        content = data["content"]
        with open(file_path, "w") as f:
            f.write(content)
        return f"✅ File written to: {file_path}"
    except Exception as e:
        return f"❌ Failed to write file: {e}"

# Available tools
available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather for the city"
    },
    "run_command": {
        "fn": run_command,
        "description": "Takes a shell command as input and executes it"
    },
    "write_file": {
        "fn": write_file,
        "description": "Takes a file_path and content, writes it to disk"
    }
}

# System prompt
system_prompt = f"""
You are CodeGenie — an intelligent AI software engineer.
You follow the loop: plan → action → observe → refine to create actual code files on disk based on the user's request.

You have tools like:
- write_file: Takes file_path and content. It writes full code files to disk.
- run_command: Run shell commands like 'uvicorn main:app --reload'.
- get_weather: (Not relevant for coding, but available)

Your goal:
1. Break down the user request into code modules or files.
2. Plan what each file should contain (e.g., main.py, routes.py, db.py).
3. Use write_file to iteratively create each file with valid code.
4. Test with run_command (like launching FastAPI).
5. Output final status or guidance to user.

Output JSON Format:
{{
    "step": "plan" | "action" | "observe" | "output",
    "content": "Your explanation or output text",
    "function": "Function name if step is action",
    "input": "Input for that function (JSON string or plain string)"
}}
"""

messages = [
    { "role": "system", "content": system_prompt }
]

# Main interactive loop
while True:
    user_query = input('👤> ')
    messages.append({ "role": "user", "content": user_query })

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )

        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        step = parsed_output.get("step")
        content = parsed_output.get("content")

        if step == "plan":
            print(f"🧠 {content}")
            continue

        if step == "action":
            function_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")

            tool = available_tools.get(function_name)
            if tool:
                output = tool["fn"](tool_input)
                messages.append({ "role": "assistant", "content": json.dumps({ "step": "observe", "output": output }) })
                continue

        if step == "output":
            print(f"🤖 {content}")
            break
