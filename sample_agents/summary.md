# How `hello_agent.py` Works — A Simple Explanation

## What Is It?
`hello_agent.py` is a minimal AI **agent** — a program that connects to Claude (an LLM by Anthropic), gives it access to a tool, and lets it decide when to use that tool to answer a question. The core idea is:

> **Agent = LLM + Tools + Loop**

---

## Step-by-Step Breakdown

### 1. 🔧 Define a Tool (`TOOLS`)
The script defines a single tool called **`calculate`**. It's described as a JSON schema so Claude knows:
- **What it does:** Evaluates a math expression.
- **What input it needs:** A string containing a Python math expression (e.g. `'2 ** 10'`).

The LLM never runs the tool itself — it only *asks* for it to be run.

### 2. ⚙️ Implement the Tool (`run_tool`)
This is the actual Python code that runs when Claude requests the `calculate` tool. It uses Python's `eval()` to compute the math expression and returns the result as a string. It also handles errors gracefully and uses a restricted `eval` (no builtins) for basic safety.

### 3. 🔁 The Agent Loop (`run_agent`)
This is the heart of the program. Here's what happens:

1. The user's message is sent to Claude along with the list of available tools.
2. Claude responds. Two things can happen:
   - **Claude is done** (`stop_reason == "end_turn"`): It has a final text answer → print it and stop.
   - **Claude wants to use a tool** (`stop_reason == "tool_use"`): It returns the tool name and inputs → the script runs the tool locally, collects the result, and sends it back to Claude.
3. The loop repeats until Claude provides a final text answer.

This back-and-forth is what makes it an *agent* rather than a simple one-shot prompt.

### 4. 🚀 Run It
When executed directly, it asks Claude:
> *"What is 2 to the power of 10, and escape velocity of earth?"*

Claude will likely:
- Use the `calculate` tool to compute `2 ** 10` → gets `1024`.
- Answer the escape velocity question from its own knowledge (no tool needed).
- Combine both into a final response.

---

## Flow Diagram

```
User Question
     │
     ▼
┌──────────┐
│  Claude   │──── Needs a tool? ── YES ──▶ Run tool locally
│  (LLM)   │◀──────────────────────────── Send result back
└──────────┘
     │
     NO (done)
     │
     ▼
  Final Answer
```

---

## Key Dependencies
| Dependency | Purpose |
|---|---|
| `anthropic` | Python SDK to talk to the Claude API |
| `python-dotenv` | Loads the API key from a `.env` file |

---

## Takeaway
This is the **simplest possible agent pattern**. Real-world agents add more tools (web search, file I/O, databases, etc.), but the loop stays the same: *let the LLM decide what to do, execute its requests, feed results back, and repeat.*
