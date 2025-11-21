# Building a minimal AI agent for terminal use and more

So you want to build your own AI agent? The good news: It's super simple, especially with more recent language models.

This tutorial will walk you through the basics to get your own agent that follows an initial prompt and can use the terminal. It's not going to use any packages (other than to query a LM), so you'll understand the entire flow.

And if you think this is too simplified and can never work in practice: Our [`mini` agent](mini-swe-agent.com) is built exactly the same (just with a bit more fluff to support more models be a bit more convenient) and it scores up to 74% on [SWE-bench verified](https://www.swebench.com/), only a few percent below highly optimized agents. 

Your final result will look like this:



## Our first prototype in 50 lines

Let's get started: From a top level view, an AI agent is just a big loop: You start with a prompt, the agent proposes an action, you execute the action, tell the LM the output, and then repeat.
To keep track of what have happend we continue to append to the `messages` list.

Pseudocode:

```python
messages = [{"role": "user", "content": "Help me fix the ValueError in main.py"}]
while True:
	lm_output = query_lm(messages)
	action = parse_action(lm_output)  # we need to separate the action from the rest of the output
	output = execute_action(action)
	print(lm_output["action"], "\n\n", output)
	# Update the message history for the next round
	messages.append({"role": .., lm_output)  # LM needs to knows what was executed in the last step
	messages.append({"role": ..., output)     # and the execution output
```

!!! what's up with the `role` field?


So to get this to work, we only need to implement two things:

1. Querying the LM API (this can get annoying if you want to support all LMs, or want detailed cost information, but is very simple if you already know which model you want)
2. Parsing the action (`parse_action`). You don't need that if you use tool calls instead (see below).
3. Executing the action (very simple)


Let's start with the first step. Click on the tabs to find the right LM for you. 

```python
def query_lm(messages):
   ...
```


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