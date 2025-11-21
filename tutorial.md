# Building a minimal AI agent for terminal use and more

So you want to build your own AI agent? The good news: It's super simple, especially with more recent language models.

This tutorial will walk you through the basics to get your own agent that follows an initial prompt and can use the terminal. It's not going to use any packages (other than to query a LM), so you'll understand the entire flow.

And if you think this is too simplified and can never work in practice: Our [`mini` agent](https://mini-swe-agent.com) is built exactly the same (just with a bit more fluff to support more models be a bit more convenient) and it scores up to 74% on [SWE-bench verified](https://www.swebench.com/), only a few percent below highly optimized agents. 

Your final result will look like this:



## Our first prototype in 50 lines

Let's get started: From a top level view, an AI agent is just a big loop: You start with a prompt, the agent proposes an action, you execute the action, tell the LM the output, and then repeat.
To keep track of what have happend we continue to append to the `messages` list.

Pseudocode:

```python
messages = [{"role": "user", "content": "Help me fix the ValueError in main.py"}]
while True:
	lm_output = query_lm(messages)
	action = parse_action(lm_output)  # separate the action from output
	output = execute_action(action)
	print(lm_output["action"], "\n\n", output)
	# Update the message history for the next round
	messages.append({"role": .., lm_output)  # remember what was executed
	messages.append({"role": ..., output)    # and the execution output
```

??? info "What's up with the `role` field?"
    The `role` field indicates who sent the message in the conversation. Common roles are:
    
    - `"user"` - Messages from the user/human
    - `"assistant"` - Messages from the AI model
    - `"system"` - System prompts that set context/instructions
    
    Different LM APIs may have slightly different conventions for how to structure these messages.


So to get this to work, we only need to implement two things:

1. Querying the LM API (this can get annoying if you want to support all LMs, or want detailed cost information, but is very simple if you already know which model you want)
2. Parsing the action (`parse_action`). You don't need that if you use tool calls instead (see below).
3. Executing the action (very simple)


Let's start with the first step. Click on the tabs to find the right LM for you.

=== "OpenAI"

    Install the OpenAI package:
    ```bash
    pip install openai
    ```

    Here's the minimal code to query the API:
    ```python
    from openai import OpenAI
    
    client = OpenAI(
        api_key="your-api-key-here"
    )  # or set OPENAI_API_KEY env var
    
    def query_lm(messages):
        response = client.chat.completions.create(
            model="gpt-5.1",
            messages=messages
        )
        return response.choices[0].message.content
    ```

=== "Anthropic"

    Install the Anthropic package:
    ```bash
    pip install anthropic
    ```

    Here's the minimal code to query the API:
    ```python
    from anthropic import Anthropic
    
    client = Anthropic(
        api_key="your-api-key-here"
    )  # or set ANTHROPIC_API_KEY env var
    
    def query_lm(messages):
        response = client.messages.create(
            model="claude-sonnet-4.5",
            max_tokens=4096,
            messages=messages
        )
        return response.content[0].text
    ```

=== "OpenRouter"

    Install the OpenAI package (OpenRouter uses OpenAI-compatible API):
    ```bash
    pip install openai
    ```

    Here's the minimal code to query the API:
    ```python
    from openai import OpenAI
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="your-api-key-here"
    )  # or set OPENROUTER_API_KEY env var
    
    def query_lm(messages):
        response = client.chat.completions.create(
            model="anthropic/claude-3.5-sonnet",  # or any model on OpenRouter
            messages=messages
        )
        return response.choices[0].message.content
    ```

=== "LiteLLM"

    Install the LiteLLM package (supports 100+ LLM providers):
    ```bash
    pip install litellm
    ```

    Here's the minimal code to query the API:
    ```python
    from litellm import completion
    
    def query_lm(messages):
        response = completion(
            model="openai/gpt-5.1",  # can be any provider + model
            messages=messages
        )
        return response.choices[0].message.content
    ```

=== "GLM"

    Install the Zhipu AI package:
    ```bash
    pip install zhipuai
    ```

    Here's the minimal code to query the API:
    ```python
    from zhipuai import ZhipuAI
    
    client = ZhipuAI(
        api_key="your-api-key-here"
    )  # or set ZHIPUAI_API_KEY env var
    
    def query_lm(messages):
        response = client.chat.completions.create(
            model="glm-4-plus",
            messages=messages
        )
        return response.choices[0].message.content
    ```

??? info "How to set environment variables"
    Instead of hardcoding your API key in the code, you can set it as an environment variable. Note that these commands set the variable only for your current terminal session (not persistent).

    === "Linux/macOS"
    
        ```bash
        export OPENAI_API_KEY="your-api-key-here"
        export ANTHROPIC_API_KEY="your-api-key-here"
        export GOOGLE_API_KEY="your-api-key-here"
        ```
        
        To make persistent, add to `~/.bashrc`, `~/.zshrc`, or your shell config file.

    === "Windows (CMD)"
    
        ```cmd
        set OPENAI_API_KEY=your-api-key-here
        set ANTHROPIC_API_KEY=your-api-key-here
        set GOOGLE_API_KEY=your-api-key-here
        ```
        
        To make persistent, use "Environment Variables" in System Properties.

    === "Windows (PowerShell)"
    
        ```powershell
        $env:OPENAI_API_KEY="your-api-key-here"
        $env:ANTHROPIC_API_KEY="your-api-key-here"
        $env:GOOGLE_API_KEY="your-api-key-here"
        ```
        
        To make persistent, use "Environment Variables" in System Properties.

Now as for executing the action, it's actually very simple, we can just use python's `subprocess` module (or just `os.system`, though that's generally less recommended)

```python
def execute_action(...):
   asdf
```

Let's put it together and run it!

## Let's make it more robust

### Handling malformatted outputs

### Handling timeouts

### Using toolcalls & adding tools

## Make it pretty & interactive

## mini-swe-agent

## Contribute to this guide

...