import anthropic
from dotenv import load_dotenv

load_dotenv()


TOOLS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to read.",
                }
            },
            "required": ["filename"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to write to.",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file.",
                },
            },
            "required": ["filename", "content"],
        },
    },
    {
        "name": "list_files",
        "description": "List all files in a directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "The directory to list files from.",
                }
            },
            "required": ["directory"],
        },
    },
    {
        "name": "search_in_file",
        "description": "Search for a query in a file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to search in.",
                },
                "query": {"type": "string", "description": "The query to search for."},
            },
            "required": ["filename", "query"],
        },
    },
    {
        "name": "run_python_file",
        "description": "Run a Python file and return its output.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the Python file to run.",
                }
            },
            "required": ["filename"],
        },
    },
]


def run_tool(name: str, inputs: dict) -> str:
    if name == "read_file":
        try:
            with open(inputs["filename"], "r") as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"
    elif name == "write_file":
        try:
            with open(inputs["filename"], "w") as f:
                f.write(inputs["content"])
            return "File written successfully."
        except Exception as e:
            return f"Error: {e}"
    elif name == "list_files":
        import os

        try:
            files = os.listdir(inputs["directory"])
            return "\n".join(files)
        except Exception as e:
            return f"Error: {e}"
    elif name == "search_in_file":
        try:
            with open(inputs["filename"], "r") as f:
                content = f.read()
                if inputs["query"] in content:
                    return "Query found in file."
                else:
                    return "Query not found in file."
        except Exception as e:
            return f"Error: {e}"
    elif name == "run_python_file":
        import subprocess

        try:
            result = subprocess.run(
                ["python", inputs["filename"]],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"
    return f"Unknown tool: {name}"


def run_agent(user_message: str):
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]

    print(f"\nUser: {user_message}\n")

    while True:
        print("Agent is thinking...\n")
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            messages=messages,
            tools=TOOLS,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            final_text = next(b.text for b in response.content if hasattr(b, "text"))
            print(f"Agent: {final_text}")
            return final_text

        if response.stop_reason == "tool_use":
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    print(f"  [tool call] {block.name}({block.input})")
                    result = run_tool(block.name, block.input)
                    print(f"  [tool result] {result}")

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    run_agent(
        "Look at the hello_agent.py file in my current folder, Execute it and store it in output.txt file"
    )
