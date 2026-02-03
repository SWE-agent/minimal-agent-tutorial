<div class="hero-title">
  <h1 class="main-title">Building a minimal AI agent from scratch</h1>
  <p class="subtitle">for software engineering, terminal use, and more</p>
</div>

<div class="author-box">
  <p><strong>Authors:</strong> Kilian Lieret, Carlos Jimenez, John Yang, Ofir Press.</p>
  <p><strong>Contributions by</strong> Cesar Garcia <a href="#contribute">Contribute</a></p>
</div>

So you want to build your own AI agent from scratch? The good news: It's super simple, especially with more recent language models.
We won't be using any external packages (other than to query the LM), and our initial minimal agent is only some 60 lines long.

And if you think this is too simplified and can never work in practice: Our [`mini` agent](https://mini-swe-agent.com) is built exactly the same, and is used for research at Princeton, Stanford, NVIDIA, Anyscale, essentials.ai and more. 
Using this simple guide you can score up to 74% on [SWE-bench verified](https://www.swebench.com/), only a few percent below highly optimized agents. 

## Our first prototype in 50 lines

Let's get started: From a top level view, an AI agent is just a big loop: You start with a prompt, the agent proposes an action, you execute the action, tell the LM the output, and then repeat.
To keep track of what have happend we continue to append to the `messages` list.

Pseudocode:

```python
messages = [{"role": "user", "content": "Help me fix the ValueError in main.py"}]
while True:
	lm_output = query_lm(messages)
    print("LM output", output)
	messages.append({"role": "assistant", "content": lm_output})  # remember what the LM said
	action = parse_action(lm_output)  # separate the action from output
    print("Action", action)
    if action == "exit":
        break
	output = execute_action(action)
    print("Output", output)
	messages.append({"role": "user", "content": output})  # send command output back
```

??? info "What's up with the `role` field?"
    The `role` field indicates who sent the message in the conversation. Common roles are:
    
    - `"user"` - Messages from the user/human
    - `"assistant"` - Messages from the AI model
    - `"system"` - System prompts that set context/instructions
    
    Different LM APIs may have slightly different conventions for how to structure these messages.


So to get this to work, we only need to implement two things:

1. Querying the LM API (this can get annoying if you want to support all LMs, or want detailed cost information, but is very simple if you already know which model you want)
2. Parsing the action (`parse_action`). You don't need this if you use the tool calling functionality of your LM if it supports it, but this is more provider-specific, so we wo'nt cover it in this guide for now (don't worry, the performance should not be impacted by this).
3. Executing the action (very simple, in our case we will simply execute any action of the LM as a bash-command in the terminal).

### Querying the LM


Let's start with the first step. Click on the tabs to find the right LM for you.
`litellm` supports most specific LMs, so this is a good default option if your LM is not explicitly mentioned.

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
        response = client.responses.create(
            model="gpt-5.1",
            input=messages
        )
        return response.output_text
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

    Alternatively, you can use a `.env` file with [python-dotenv](https://pypi.org/project/python-dotenv/).

??? info "Type hints in python"

    In case you're wondering about the `list[dict[str, str]]` and the `-> str` in the
    previous code example, these are "type hints" and they are optional in python,
    but they help your IDE or static checker (or even just yourself) to understand
    the inputs and outputs of the function.

??? example "Let's test it"
    Here's a quick test to verify your LM query function works:
    
    ```python
    messages = [{"role": "user", "content": "Roll a d20"}]
    print(query_lm(messages))
    ```
    
    You should see the model's response, something like a dice roll result or explanation!

??? info "In production"
    If you want to see how this is done in production, check out the model classes in [mini](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/models/):

    
    - [LiteLLM model](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py)
    - [OpenRouter model](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/models/openrouter_model.py)

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

??? info "In production"
    If you want to see how this is done in production, check out the [parse_action implementation in default.py](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py) in mini-swe-agent.


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
        timeout=30,
    )
    return result.stdout
```


??? info "Understanding `subprocess.run` arguments"
    Let's break down the keyword arguments we're using:
    
    - `shell=True` - Allows running arbitrary shell commands given as a string (like `cd`, `ls`, pipes, etc.). Be careful with untrusted input!
    - `text=True` - Returns output as strings instead of bytes
    - `env=os.environ` - Passes the current environment variables to the subprocess
    - `encoding="utf-8"` - Specifies UTF-8 encoding for text output
    - `errors="replace"` - Replaces invalid characters instead of raising errors
    - `stdout=subprocess.PIPE` - Captures standard output
    - `stderr=subprocess.STDOUT` - Redirects stderr to stdout (so we capture both in one stream)
    - `timeout=30`: Stop executing after

??? info "In production"
    If you want to see how this is done in production, check out mini-swe-agent's environment classes:
    
    - [Local environment](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/environments/local.py) - the closest equivalent to the code above
    - [Docker environment](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/environments/docker.py) - almost the same as local, except commands are executed via `docker exec` instead of `subprocess.run`

There are a couple of limitations to this:

1. The agent will not be able to `cd` to a different environment
2. The agent cannot persist environment variables easily

However, in practice, we have found these limitations to be not very limiting at all.
In fact, reducing the amount of hidden state and forcing the agent to work with absolute paths might well be helpful for language models in many instances.
It is also similar with `ClaudeCode` (while it can change directories, it cannot persist environment variables, because it similarly uses subshells to execute commands).

### Add a system prompt

We still need to tell the LM a bit more about how to behave:

```python
messages = [{
    "role": "system", 
    "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command."
}
]
```

### Let's put it together & run it!

You should now have code that looks something like this (this example uses litellm + triple backticks):

```python linenums="1"
import re
import subprocess
import os
from litellm import completion

def query_lm(messages: list[dict[str, str]]) -> str:
    response = completion(
        model="openai/gpt-5.1",
        messages=messages
    )
    return response.choices[0].message.content

def parse_action(lm_output: str) -> str:
    """Take LM output, return action"""
    matches = re.findall(
        r"```bash-action\s*\n(.*?)\n```", 
        lm_output, 
        re.DOTALL
    )
    return matches[0].strip() if matches else ""

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
        timeout=30,
    )
    return result.stdout

# Main agent loop
messages = [{
    "role": "system", 
    "content": "You are a helpful assistant. When you want to run a command, wrap it in ```bash-action\n<command>\n```. To finish, run the exit command."
}, {
    "role": "user", 
    "content": "List the files in the current directory"
}]

while True:
	lm_output = query_lm(messages)
    print("LM output", lm_output)
	messages.append({"role": "assistant", "content": lm_output})  # remember what the LM said
	action = parse_action(lm_output)  # separate the action from output
    print("Action", action)
    if action == "exit":
        break
	output = execute_action(action)
    print("Output", output)
	messages.append({"role": "user", "content": output})  # send command output back
```

## Let's make it more robust

The following sections are some tweaks to improve performance.
Nothing fancy, just making sure that the agent doesn't get stuck and can deal with things that go wrong.
This section is a bit more advanced.
Instead of showing the complete code at the end, we encourage everyone to check out the [source code](https://github.com/SWE-agent/mini-swe-agent/) of our `mini` agent; it includes all of these features with very little fluff around it (also see the next section to get started with reading the code).

### Dealing with exceptions in the control flow

The idea here: Whenever a known exception arises (timeouts, format errors, etc.), let's just tell the LM and let it handle it itself. This means adapting our `while` loop a bit:

```python
while True:
    try:
        # previous content
    except Exception as e:
        messages.append({"role": "user", "content": str(e)})
```

That's it!

For example, if the agent does something stupid (like calling `vim`) and a `TimeoutError` is triggered, this will cause the error message to be appended to the messages and the
LM can pick up from there, hopefully realizing what it did wrong.

However, we might only limit this behavior to some known problems or add more information to the message. In this case, we can be more specific, for example

```python
class OurTimeoutError(RuntimeError): ...

def execute_action(action: str) -> str:
    try:
        # as before
    except TimeoutError as e:
        raise OurTimeoutError("Your last command time out, you might want to ...") from e
```

and just like this, we've added additional information for the LM.

You might also want to be more specific with what exceptions are handed to the LM and which just cause the program to crash. In this case it might make sense to define a custom exception class and only catch that in the `while` loop:

```python
class NonterminatingException(RuntimeError): ...
class OurTimeoutError(NonterminatingException): ...

while True:
    try: 
        ...
    except NonterminatingException as e:
        ...
```

mini-swe-agent additionally [defines](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py#L33-L53) a `TerminatingException` class which is used instead of the `if action == "exit"` mechanism to stop the `while` loop in a graceful way:

```python
class TerminatingException(RuntimeError): ...
class Submitted: ...  # agent wants to stop

def execute_action(action: str) -> str:
    if action == "exit":
        raise TerminatingException("LM requested to quit")
    ...

while True:
    try:
        ...
    except NonterminatingException as e:
        ...
    except TerminatingException as e:
        print("Stopping because of ", str(e))
        break
```

### Handling malformatted outputs

Sometimes (especially with weaker LMs), the LM will not properly format it's action.
It's good to remind it about the correct way in that case:
This should be very straightforward now that we have the general exception handling in place:

````python
incorrect_format_message = """Your output was malformated.
Please include exactly 1 action formatted as in the following example:

```bash-action
ls -R
```
"""
class FormatError(RuntimeError): ...

def parse_action(action: str) -> str:
   matches = ...
   if not len(matches) == 1:
       raise FormatError(incorrect_format_message)
   ...
````

### Environment variables

There's a couple of environment variables that we can set to disable interactive
elements in command line tools that avoid the agent getting stuck (you can see them being set in the [`mini-swe-agent` SWE-bench config](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/config/extra/swebench.yaml)):

```python
env_vars = {
    PAGER: cat
    MANPAGER: cat
    LESS: -R
    PIP_PROGRESS_BAR: 'off'
    TQDM_DISABLE: '1'
}

# ...

def execute_action(command: str) -> str:
    # ...
    result = subprocess.run(
        command,
        # ...
        env=os.environ | env_vars
        # ...
)
```


## mini-swe-agent

[`mini-swe-agent`](https://github.com/swe-agent/mini-swe-agent) is built exactly according to the blueprint of this tutorial and it should be very easy for you to understand it's source code.
The only important thing to note is that it is built more modular, so that you can swap out all components.

The `Agent` class ([full code](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/agents/default.py)) contains the big `while` loop in the `run` function

```python
class Agent:
    def __init__(self, model, environment):
        self.model = model
        self.environment = environment
        ... 
    
    def run(self, task: str):
        while True:
            ...
```

The model class ([example for litellm](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/models/litellm_model.py)) handles different LMs

```python
class Model:
    def query(messages: list[dict[str, str]]):
        ...
```

and the environment class ([local environment](https://github.com/swe-agent/mini-swe-agent/blob/main/src/minisweagent/environments/local.py)) executes actions:

```python
class Environment:
    def execute(command: str):
        ...
```

`mini-swe-agent` provides different environment classes that for example allow to execute actions in docker containers instead of directly in your local environment.
Sonds more complicated? It really isn't: all we do is switch from `subprocess.run` to calls to `docker exec`.

## Contribute to this guide

We welcome contributions [on GitHub](https://github.com/swe-agent/minimal-agent-tutorial) to improve this guide! 

??? Contribution guidelines

    The following PRs will be merged immediately

    - Bug fixes
    - Typo fixes

    The following PRs are much appreciated and will most likely be merged fast:

    - Adding support to popular LMs that aren't mentioned yet (please make sure test your implementation)

    The following things should be discussed first (via github issue):

    - Additional sections
    - Significant expansions of sections

    Please understand that the larger your changes are, the more time we will need to review and the less likely it is we can accept them (unless we discussed beforehand).

    To contribute:

    - Fork the repository
    - Make your changes
    - Submit a pull request

    You can find the source code on GitHub.

If you have questions or comments, please comment below. Note that [GitHub issues](https://github.com/swe-agent/minimal-agent-tutorial/issues) are still preferred for bug reports and discussions about further developing this page.

## Comments

<script src="https://giscus.app/client.js"
        data-repo="swe-agent/minimal-agent-tutorial"
        data-repo-id="R_kgDOQaid2A"
        data-mapping="number"
        data-term="1"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="preferred_color_scheme"
        data-lang="en"
        crossorigin="anonymous"
        async>
</script>
