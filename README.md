# 🤖 AI Agent

A command-line AI agent built with Python and Google's Gemini API, developed as part of the [boot.dev](https://www.boot.dev) AI Agent course. The agent can reason through tasks autonomously by calling tools in a loop — reading files, writing files, and executing Python code — until it arrives at a final answer.

---

## How It Works

The agent follows a **ReAct-style** (Reason + Act) loop:

1. You provide a natural language prompt via the CLI.
2. The agent sends it to **Gemini 2.5 Flash** along with a system prompt and a set of available tools.
3. If Gemini decides to call a tool, the agent executes it and feeds the result back.
4. The loop repeats (up to `MAX_ITERS`) until Gemini returns a final text response.

```
User prompt → Gemini → tool call? → execute → feed result back → repeat
                    ↘ final text response → print & exit
```

---

## Features

- **Agentic loop** — iterates automatically until the task is done or the iteration limit is hit
- **File system tools** — list files, read file contents, and write new/updated files
- **Code execution** — run Python scripts directly from within the agent loop
- **Verbose mode** — inspect token usage and function call arguments at each step
- **Configurable working directory** — the agent operates inside a sandboxed directory

---

## Project Structure

```
aiagent/
├── main.py                  # Entry point — CLI arg parsing and the agent loop
├── call_function.py         # Tool dispatcher — maps function names to implementations
├── prompts.py               # System prompt definition
├── config.py                # Configuration (WORKING_DIR, MAX_ITERS)
├── functions/
│   ├── get_files_info.py    # Tool: list files and metadata in a directory
│   ├── get_file_content.py  # Tool: read a file's contents
│   ├── run_python_file.py   # Tool: execute a Python script
│   └── write_file.py        # Tool: create or overwrite a file
├── calculator/              # Sample project the agent can work with
├── test_*.py                # Unit tests for each tool
├── pyproject.toml           # Project dependencies
└── .python-version          # Python version pin
```

---

## Prerequisites

- Python 3.11+
- A [Google AI Studio](https://aistudio.google.com/) API key with access to Gemini

---

## Installation

```bash
# Clone the repository
git clone https://github.com/soloHub/aiagent.git
cd aiagent

# Install dependencies (using uv — recommended)
uv sync

# Or with pip
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

The agent will raise a `RuntimeError` at startup if this key is missing.

---

## Usage

```bash
# Basic usage
python main.py "your task here"

# With verbose output (shows token counts and function call details)
python main.py "your task here" --verbose
```

**Example:**

```bash
python main.py "Look at the calculator directory and fix any bugs in the code"
```

```bash
python main.py "Create a Python script that prints the first 10 Fibonacci numbers" --verbose
```

---

## Available Tools

| Tool | Description |
|---|---|
| `get_files_info` | Lists files and directories with metadata (size, type) |
| `get_file_content` | Reads and returns the full text content of a file |
| `write_file` | Creates or overwrites a file with given content |
| `run_python_file` | Executes a Python file and returns its stdout/stderr |

All tools operate within a configured `WORKING_DIR` for safety.

---

## Running Tests

```bash
python -m pytest test_get_files_info.py test_get_file_content.py test_write_file.py test_run_python_file.py
```

---

## Built With

- [Google Gemini API](https://ai.google.dev/) (`gemini-2.5-flash`) — the LLM powering the agent
- [google-genai](https://pypi.org/project/google-genai/) — official Python SDK
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management
- [uv](https://github.com/astral-sh/uv) — fast Python package manager

---

## Course

This project was built following the [Build an AI Agent](https://www.boot.dev) course on boot.dev, which teaches how to construct autonomous agents from scratch using real LLM APIs and tool-calling patterns.

---

## License

This project is for educational purposes. Feel free to fork and experiment!