<div class="hero-title">
  <h1 class="main-title">Building a minimal AI agent</h1>
  <p class="subtitle">for terminal use and more</p>
</div>

<div class="author-box">
  <p><strong>Authors:</strong> Kilian Lieret, Carlos Jimenez, John Yang, Ofir Press.</p>
  <p><strong>Contributions by</strong> <a href="#contribute">Contribute</a></p>
</div>

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
2. Parsing the action (`parse_action`). You don't need this if you use the tool calling functionality of your LM if it supports it, but this is more provider-specific, so we won'nt cover it in this guide (don'tn worry, the performance should not be impacted by this).
3. Executing the action (very simple)

### Querying the LM


Let's start with the first step. Click on the tabs to find the right LM for you.

=== "OpenAI"

    Install the [OpenAI package](https://pypi.org/project/openai/) ([docs](https://platform.openai.com/docs/api-reference)):
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

    Install the [Anthropic package](https://pypi.org/project/anthropic/) ([docs](https://docs.anthropic.com/en/api)):
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

    Install the [OpenAI package](https://pypi.org/project/openai/) ([OpenRouter docs](https://openrouter.ai/docs)) - OpenRouter uses OpenAI-compatible API:
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

    Install the [LiteLLM package](https://pypi.org/project/litellm/) ([docs](https://docs.litellm.ai/)) - supports 100+ LLM providers:
    ```bash
    pip install litellm
    ```

    Here's the minimal code to query the API:
    ```python
    from litellm import completion
    
    def query_lm(messages: list[dict[str, str]]) -> str:
        response = completion(
            model="openai/gpt-5.1",  # can be any provider + model
            messages=messages
        )
        return response.choices[0].message.content
    ```

=== "GLM"

    Install the [Zhipu AI package](https://pypi.org/project/zhipuai/) ([docs](https://open.bigmodel.cn/dev/api)):
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

??? info "Type hints in python"

    In case you're wondering about the `list[dict[str, str]]` and the `-> str` in the
    previous code example, these are "type hints" and they are optional in python,
    but they help your IDE or static checker (or even just yourself) to understand
    the inputs and outputs of the function.

### Parse the action

Let's parse the action. There's two simple ways in which the LM can "encode" the action (again, you don't need this if you use tool calls, but in this tutorial we'll keep it simpler):

=== "Triple-backticks"

    This is inspired by markdown codeblocks:

        Some thoughts of the LM explaining the action and the action below

        ```bash-action
        cd /path/to/project && ls
        ```

=== "XML-style"

    ```
    Some thoughts of the LM explaining the action and the action below

    <bash_action>cd /path/to/project && ls</bash_action>
    ```

For most models, either way works well and we recommend using triple backticks.
However, some models (especially small or open source models) are slightly less general and you might try either.
Here's a quick regular expression to parse the action:


=== "Triple-backticks"
    
    ```python
    import re
    
    def parse_action(lm_output: str) -> str:
        """Take LM output, return action"""
        matches = re.findall(
            r"```bash-action\s*\n(.*?)\n```", 
            lm_output, 
            re.DOTALL
        )
        return matches[0].strip() if matches else ""
    ```
    
    ??? example "Let's test it"
        Here's a quick test to verify our parsing function works correctly:
        
        ````python
        test_output = """I'll list the files in the current directory.

        ```bash-action
        ls -la
        ```
        """

        print(parse_action(test_output))
        ````

=== "XML-style"
    
    ```python
    import re
    
    def parse_action(lm_output: str) -> str:
        """Take LM output, return action"""
        matches = re.findall(
            r"<bash_action>(.*?)</bash_action>", 
            lm_output, 
            re.DOTALL
        )
        return matches[0].strip() if matches else ""
    ```
    
    ??? example "Let's test it"
        Here's a quick test to verify our parsing function works correctly:
        
        ```python
        test_output = """I'll list the files in the current directory.
        
        <bash_action>ls -la</bash_action>
        """
        
        print(parse_action(test_output))
        ```

??? info "Understanding the regular expression"
    
    - `r"..."` - **Raw string**: The `r` prefix makes it a raw string, so backslashes are treated literally. Without it, you'd need to write `\\n` instead of `\n`, `\\s` instead of `\s`, etc.
    - `(.*?)` - **Capturing group** with non-greedy matching: The parentheses `()` capture the content we want to extract. The `.*?` matches any characters, but `?` makes it stop at the first closing pattern (non-greedy) rather than the last.
    - `re.DOTALL` flag - Makes `.` match newlines too, allowing multi-line commands to be captured.
    
    `findall` returns only what's inside the parentheses, not the surrounding markers.

### Execute the action

Now as for executing the action, it's actually very simple, we can just use python's `subprocess` module (or just `os.system`, though that's generally less recommended)

```python
import subprocess
import os

def execute_action(command: str) -> str:
    """Execute action, return output"""
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        env=os.environ,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return result.stdout
```

??? info "Understanding `subprocess.run arguments`"
    Let's break down the keyword arguments we're using:
    
    - `shell=True` - Allows running arbitrary shell commands given as a string (like `cd`, `ls`, pipes, etc.). Be careful with untrusted input!
    - `text=True` - Returns output as strings instead of bytes
    - `env=os.environ` - Passes the current environment variables to the subprocess
    - `encoding="utf-8"` - Specifies UTF-8 encoding for text output
    - `errors="replace"` - Replaces invalid characters instead of raising errors
    - `stdout=subprocess.PIPE` - Captures standard output
    - `stderr=subprocess.STDOUT` - Redirects stderr to stdout (so we capture both in one stream)

Let's put it together and run it!

### Let's run it!

You should now have code that looks something like this (this example uses litellm + triple backticks):

```python

```

## Let's make it more robust

### Handling malformatted outputs

### Handling timeouts

### Using toolcalls & adding tools

## Make it pretty & interactive

## mini-swe-agent

<h2 id="contribute">Contribute to this guide</h2>

We welcome contributions to improve this guide! Whether it's fixing typos, adding examples, or expanding sections, your input is valuable.

To contribute:
- Fork the repository
- Make your changes
- Submit a pull request

You can find the source code on GitHub.