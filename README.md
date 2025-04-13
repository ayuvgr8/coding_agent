
# CodeGenie - Intelligent AI Software Engineer

CodeGenie is an intelligent AI-powered software engineering assistant designed to help users create, refine, and execute code files on disk. It follows a structured loop of **plan → action → observe → refine** to iteratively generate and test code based on user requests.

## Features

- **Write Files**: Create code files on disk with the `write_file` tool.
- **Run Shell Commands**: Execute shell commands directly from the assistant.
- **Weather Info (Demo)**: Fetch current weather information for a given city.
- **Interactive Loop**: Engage in a conversational loop to break down tasks, generate code, and refine outputs.

## How It Works

1. **User Input**: Provide a request or task to CodeGenie.
2. **Planning**: CodeGenie breaks down the task into smaller modules or files.
3. **Action**: It uses tools like `write_file` to create files or `run_command` to execute commands.
4. **Observation**: CodeGenie observes the results and refines the output as needed.
5. **Output**: The final result is presented to the user.

## Tools Available

- **`write_file`**: Writes a file to disk with the specified content.
- **`run_command`**: Executes shell commands.
- **`get_weather`**: Fetches weather information for a city (for demo purposes).

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>