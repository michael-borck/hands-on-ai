# AiLabKit Command Line Interface (CLI)

This document provides a reference for the command-line interfaces in AiLabKit. The toolkit provides several CLI commands for different modules.

## Main CLI (ailabkit)

The main `ailabkit` command provides access to global functions and serves as an entry point to the module-specific commands.

```bash
Usage: ailabkit [OPTIONS] COMMAND [ARGS]...

  AI Learning Lab Toolkit

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy
                        it or customize the installation.
  --help                Show this message and exit.

Commands:
  version   Display version information
  list      List available modules
  doctor    Check environment and configuration
  config    View or edit configuration
```

### Example Usage

```bash
# Check system configuration
ailabkit doctor

# View and edit configuration
ailabkit config

# List all available modules
ailabkit list

# Check version
ailabkit version
```

## Chat Module CLI (chat)

The `chat` module provides an interface for interacting with various bot personalities.

```bash
Usage: chat [OPTIONS] COMMAND [ARGS]...

  Simple chatbot with personality

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy
                        it or customize the installation.
  --help                Show this message and exit.

Commands:
  ask           Send a single prompt to a bot
  bots          List available bots
  doctor        Run diagnostics
  interactive   Start interactive REPL
  web           Launch web interface
```

### Example Usage

```bash
# List all available bot personalities
chat bots

# Ask a question with a specific bot personality
chat ask --personality pirate_bot "Tell me about the weather"

# Start an interactive chat session
chat interactive

# Launch the web interface for chat
chat web
```

## RAG Module CLI (rag)

The `rag` (Retrieval-Augmented Generation) module provides tools for document indexing and question answering.

```bash
Usage: rag [OPTIONS] COMMAND [ARGS]...

  RAG - Retrieval-Augmented Generation

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy
                        it or customize the installation.
  --help                Show this message and exit.

Commands:
  index         Build a RAG index from files
  ask           Ask questions using indexed documents
  interactive   Run interactive RAG chat
  web           Launch web interface for RAG
```

### Example Usage

```bash
# Index a directory of documents
rag index docs/

# Ask a question using the indexed documents
rag ask "What is the purpose of RAG?"

# Start an interactive RAG session
rag interactive

# Launch the web interface for RAG
rag web
```

### Detailed Command Options

#### rag index

```bash
Usage: rag index [OPTIONS] INPUT_PATH

  Build a RAG index from files

Arguments:
  INPUT_PATH  File or directory to index [required]

Options:
  --output-file TEXT          Output index file (default: ~/.ailabkit/index.npz)
  --chunk-size INTEGER        Words per chunk (default: from config)
  --force / --no-force        Overwrite existing index [default: no-force]
  --help                      Show this message and exit.
```

## Agent Module CLI (agent)

The `agent` module provides tools for working with AI agents that can use tools to perform tasks.

```bash
Usage: agent [OPTIONS] COMMAND [ARGS]...

  Agent - LLM Tool Use & Reasoning

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy
                        it or customize the installation.
  --help                Show this message and exit.

Commands:
  ask           Run an agent with a prompt
  tools         List available tools
  interactive   Start interactive agent console
  web           Launch web interface for agent
```

### Example Usage

```bash
# List available agent tools
agent tools

# Run an agent with a specific prompt
agent ask "What is 25 * 32?"

# Start an interactive agent session
agent interactive

# Launch the web interface for the agent
agent web
```

## Tips for Using the CLI

1. All commands support the `--help` flag to display available options
2. Use tab completion (if installed) for easier navigation
3. The web interfaces provide a graphical alternative to the command-line
4. The interactive modes (REPL) allow for multi-turn conversations
5. Configure settings in `~/.ailabkit/config.json` or with the `ailabkit config` command
