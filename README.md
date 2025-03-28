# Multi-LLM Manager

## Overview

Multi-LLM Manager is a Python package that enables seamless interaction with multiple free-tier language model (LLM) providers.

## Installation

```bash
pip install APIShift
```

## Quick Start

```python
from APIShift import Conversation
from APIShift import GeminiProvider, OpenRouterProvider

# Initialize providers with API keys
gemini_keys = ['your_gemini_api_key1', 'your_gemini_api_key2']
openrouter_keys = ['your_openrouter_api_key1', 'your_openrouter_api_key2']

# Create a conversation with multiple providers
conversation = Conversation([
    GeminiProvider(gemini_keys),
    OpenRouterProvider(openrouter_keys)
])

# Send messages
response = conversation.send_message("Hello, how are you?")
print(response)
```

## More details coming soon...
