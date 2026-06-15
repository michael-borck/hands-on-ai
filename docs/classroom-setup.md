# Classroom Setup for HandsOnAI

This guide walks educators and students through the technical setup needed to use [HandsOnAI](https://github.com/michael-borck/hands-on-ai) in a classroom environment. It assumes basic familiarity with Python and supports any OpenAI-compatible LLM provider.

---

## 💻 System Requirements

- Operating System: Linux, macOS, or WSL on Windows
- Python: 3.10+
- Access to an OpenAI-compatible LLM provider:
  - Local: [Ollama](https://ollama.com) for privacy and control
  - Cloud: OpenAI, OpenRouter, Together AI, etc. for advanced models
- Internet access (for installation and cloud providers)

---

## 🔧 Installation Steps

### Option 1: Simple Installation (Recommended for Students)
```bash
pip install hands-on-ai
```

### Option 2: Development Installation (Recommended for Educators)

#### 1. Clone the HandsOnAI Repository
```bash
git clone https://github.com/michael-borck/hands-on-ai.git
cd hands-on-ai
```

#### 2. Create a Virtual Environment
We recommend `uv` for fast installs, but `venv` or `virtualenv` also works.
```bash
uv venv .venv
source .venv/bin/activate
```

#### 3. Install HandsOnAI (Editable Mode)
```bash
uv pip install -e '.[dev]'
```
This installs the core package, CLI entry points, and development tools.

---

## 🌍 Provider Configuration

HandsOnAI works with any OpenAI-compatible provider. Choose the best option for your classroom:

### Option 1: Local Ollama (Privacy & Control)
Best for: Schools concerned about data privacy, offline environments

1. Install Ollama: [https://ollama.com/download](https://ollama.com/download)
2. Start the server: `ollama run llama3`
3. No additional configuration needed - HandsOnAI defaults to `http://localhost:11434`

### Option 2: Shared Classroom Server (Recommended)
Best for: Centralized management, consistent performance

```python
import os
os.environ['HANDS_ON_AI_SERVER'] = 'https://your-classroom-server.edu'
os.environ['HANDS_ON_AI_API_KEY'] = input('Enter your API key: ')
```

### Option 3: Cloud Providers (Advanced Models)
Best for: Access to latest models, minimal setup

```python
import os
# OpenAI
os.environ['HANDS_ON_AI_SERVER'] = 'https://api.openai.com'
os.environ['HANDS_ON_AI_API_KEY'] = 'sk-your-openai-key'

# Or OpenRouter (access to many models)
os.environ['HANDS_ON_AI_SERVER'] = 'https://openrouter.ai/api'  
os.environ['HANDS_ON_AI_API_KEY'] = 'sk-or-your-key'
os.environ['HANDS_ON_AI_MODEL'] = 'openai/gpt-4'
```

---

## 🚀 Test the Setup

### Quick Python Test:
```python
from hands_on_ai.chat import get_response
print(get_response("Hello! Are you working?"))
```

### CLI Check:
```bash
handsonai doctor
```
Should report that your provider is reachable and show available models.

### Module Tests:
```bash
# Test chat module
chat "Tell me a joke"

# Test agent module  
agent "What is 15 * 23? Use the calculator tool"

# Test RAG module
rag ask "What is machine learning?" --docs path/to/documents/
```

---

## 🧪 Classroom Preparation Checklist

### For Local Ollama Setup:
- ✅ Ensure all students have Python 3.10+ installed
- ✅ Install Ollama on lab machines or student laptops
- ✅ Pre-download models if bandwidth is limited: `ollama pull llama3`
- ✅ Test with `handsonai doctor` on each machine

### For Centralized Server Setup:
- ✅ Set up OpenAI-compatible server with authentication
- ✅ Generate API keys for each student or class
- ✅ Provide students with server URL and API keys
- ✅ Test connection from student machines

### For Cloud Provider Setup:
- ✅ Set up accounts with chosen provider (OpenAI, OpenRouter, etc.)
- ✅ Configure billing and usage limits
- ✅ Distribute API keys securely to students
- ✅ Monitor usage to avoid unexpected costs

---

## 🎓 Student Setup Instructions

Provide students with this simple setup script:

```python
# hands_on_ai_setup.py
import os

# Configuration (update with your classroom details)
os.environ['HANDS_ON_AI_SERVER'] = 'https://your-classroom-server.edu'
os.environ['HANDS_ON_AI_MODEL'] = 'llama3'

# Get API key securely
api_key = input('Enter your API key: ')
os.environ['HANDS_ON_AI_API_KEY'] = api_key

# Test the setup
try:
    from hands_on_ai.chat import get_response
    response = get_response("Hello! Confirm you're working correctly.")
    print("✅ Setup successful!")
    print(f"Response: {response}")
except Exception as e:
    print(f"❌ Setup failed: {e}")
    print("Please check your configuration and try again.")
```

---

## 🧰 Related Tools & Commands

### Diagnostic Commands
- `handsonai doctor` - Check provider connection and configuration
- `handsonai --help` - View CLI options

### Module Commands
- `chat --help` - Chat module help and options
- `agent --help` - Agent module help and options  
- `rag --help` - RAG module help and options

### Development Tools (if using dev installation)
- `pytest` - Run test suite
- `mkdocs serve` - Live preview of documentation site
- `ruff check` - Code linting

---

## 🎯 Quick Troubleshooting

### "Connection refused" or "404 errors"
- ✅ Check if your provider server is running
- ✅ Verify the server URL is correct
- ✅ Confirm API key is valid (if required)
- ✅ Check firewall settings for classroom servers

### "Model not found" errors
- ✅ Verify model name matches provider's format
- ✅ For Ollama: run `ollama pull model-name` first
- ✅ For cloud providers: check available models in their docs

### Slow responses
- ✅ Try a smaller/faster model
- ✅ Check network connection for cloud providers
- ✅ Consider using local Ollama for faster responses

---

## 📚 See Also
- [Configuration Guide](configuration.md) - Detailed configuration options
- [Ollama Guide](ollama-guide.md) - Local Ollama setup instructions  
- [Education Guide](education-guide.md) - Pedagogical guidance
- Provider Compatibility (see main README) - Supported providers

