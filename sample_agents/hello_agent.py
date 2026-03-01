"""
Hello World Agent
=================
The simplest possible agent: an LLM in a loop that can call tools.

Agent = LLM + Tools + Loop
"""

import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── 1. Define tools ───────────────────────────────────────────────────────────
# Tools are just JSON schemas that describe what the LLM can call.
# You write the actual implementation; the LLM just decides *when* to call them.

TOOLS = [
    {
        "name": "calculate",
        "description": "Evaluate a mathematical expression and return the result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "A Python math expression, e.g. '2 ** 10' or '(3 + 5) * 7'",
                }
            },
            "required": ["expression"],
        },
    }
]


# ── 2. Implement tools ────────────────────────────────────────────────────────
# The LLM picks a tool and sends back its name + arguments.
# You run the actual code and send the result back.


def run_tool(name: str, inputs: dict) -> str:
    if name == "calculate":
        try:
            result = eval(inputs["expression"], {"__builtins__": {}}, {})
            return str(result)
        except Exception as e:
            return f"Error: {e}"
    return f"Unknown tool: {name}"


# ── 3. The agent loop ─────────────────────────────────────────────────────────
# This is the core of every agent:
#   LLM responds → if it wants to use a tool, run it → send result back → repeat


def run_agent(user_message: str):
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": user_message}]

    print(f"\nUser: {user_message}\n")

    while True:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        # Add the assistant's response to the conversation history
        messages.append({"role": "assistant", "content": response.content})

        # Case 1: LLM is done — it returned a final text answer
        if response.stop_reason == "end_turn":
            final_text = next(b.text for b in response.content if hasattr(b, "text"))
            print(f"Agent: {final_text}")
            return final_text

        # Case 2: LLM wants to call a tool
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

            # Send tool results back so the LLM can continue
            messages.append({"role": "user", "content": tool_results})


# ── 4. Run it ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_agent("What is 2 to the power of 10, and escape velocity of earth?")
