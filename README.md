# Eleminder AI - GitHub Code Assistant

An intelligent code assistant that integrates LLM (Large Language Model) with GitHub through the Model Context Protocol (MCP). Allows you to ask natural questions about repositories, organizations, and GitHub code.

## 🚀 Features

- **Natural GitHub questions**: Ask questions in natural language about repositories, issues, pull requests, etc.
- **OpenAI integration**: Uses GPT-5 to process and answer questions
- **Direct GitHub access**: Connects directly to GitHub API via MCP
- **Command line interface**: Simple and direct for developers

## 📋 Prerequisites

### Required API Keys:

```bash
# OpenAI API Key
export OPENAI_API_KEY="your_openai_key_here"

# GitHub Personal Access Token
export GITHUB_TOKEN="your_github_token_here"

# GitHub Login (required)
export GITHUB_LOGIN="your_github_username"
```

### How to get the keys:

1. **OpenAI API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key

2. **GitHub Token**:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a token with permissions to access repositories and organizations

3. **GitHub Login**:
   - Use your GitHub username (the one that appears in your profile URL)
   - Example: if your profile is `github.com/yourusername`, use `yourusername`

### Docker (for MCP GitHub Server):
```bash
# Make sure Docker is running
docker --version
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd eleminder-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install pre-commit hooks (optional but recommended):
```bash
pre-commit install
```

4. Configure environment variables (see prerequisites section)

## 🔧 Pre-commit Setup

This project uses pre-commit hooks to ensure code quality. After installing dependencies, run:

```bash
# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files (first time)
pre-commit run --all-files
```

### What pre-commit does:
- **Code formatting**: Automatically formats Python code with Ruff
- **Linting**: Checks for code issues and fixes them automatically
- **File checks**: Removes trailing whitespace, fixes end-of-file issues
- **YAML validation**: Ensures configuration files are valid
- **Large file detection**: Prevents accidentally committing large files

### Manual usage:
```bash
# Run pre-commit on staged files only
pre-commit run

# Run pre-commit on all files
pre-commit run --all-files

# Update pre-commit hooks to latest versions
pre-commit autoupdate
```

## 🎯 How to use

### Basic execution:
```bash
# Interactive mode (recommended)
python main.py

# With initial question
python main.py "What organizations am I part of?"
```

### Example questions you can ask:

#### About organizations:
```bash
python main.py "What organizations am I part of?"
python main.py "List all repositories in the 'my-org' organization"
python main.py "How many members does the 'github' organization have?"
```

#### About repositories:
```bash
python main.py "Show the latest commits from repository 'user/repo'"
python main.py "What are the open issues in repository 'facebook/react'?"
python main.py "List contributors of repository 'microsoft/vscode'"
```

#### About pull requests:
```bash
python main.py "Show open PRs in repository 'torvalds/linux'"
python main.py "What PRs were closed this week in repo 'nodejs/node'?"
```

#### About issues:
```bash
python main.py "List issues with 'bug' label in repository 'kubernetes/kubernetes'"
python main.py "Show the oldest issues in repository 'golang/go'"
```

#### About code:
```bash
python main.py "Find Python files in repository 'django/django'"
python main.py "Show the folder structure of repository 'tensorflow/tensorflow'"
```

#### About releases:
```bash
python main.py "What were the latest releases of repository 'python/cpython'?"
python main.py "Show the release notes for Python v3.12.0"
```

### Interactive Mode (Recommended):
The assistant now runs in interactive mode by default, maintaining conversation context:

```bash
python main.py
```

**Features:**
- **Conversation context**: The assistant remembers previous questions and answers
- **Continuous dialogue**: Ask follow-up questions naturally
- **Easy exit**: Type `exit`, `quit`, `bye`, or `q` to end the conversation
- **Keyboard shortcuts**: Use `Ctrl+C` to exit anytime

**Example session:**
```
🤖 GitHub Code Assistant - Interactive Mode
Type 'exit', 'quit', or 'bye' to end the conversation
==================================================

User: What organizations am I part of?

🤖 Assistant: You are part of the following organizations:
- microsoft
- github
- tensorflow

User: Show me the latest commits from the microsoft/vscode repository

🤖 Assistant: Here are the latest commits from microsoft/vscode:
- commit abc123: Fix TypeScript error handling
- commit def456: Update documentation

User: exit
👋 Goodbye!
```

## 🏗️ Architecture

```
eleminder-ai/
├── main.py                 # Application entry point
├── code_assistant.py       # Main assistant class
├── llm/                    # LLM components
│   ├── open_ai_llm.py     # OpenAI client
│   ├── prompt_loader.py    # Prompt loader
│   └── prompts/           # Prompt files
├── mcp_components/         # MCP components
│   ├── mcp_host.py        # MCP host
│   ├── github_mcp_client.py # GitHub MCP client
│   └── mcp_response_formatter.py # Response formatter
└── utils/                 # Utilities
```

## 🔧 Advanced Configuration

### Customize the assistant:
Edit `llm/prompts/natural-github.txt` to modify the assistant's behavior.

### Add new tools:
Modify `llm/prompts/tools.json` to include new GitHub capabilities.

## 🐛 Troubleshooting

### MCP connection error:
```bash
# Check if Docker is running
docker ps

# Test connection manually
docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=$GITHUB_TOKEN ghcr.io/github/github-mcp-server
```

### API Key error:
```bash
# Check if variables are set
echo $OPENAI_API_KEY
echo $GITHUB_TOKEN
```

## 📝 Output Examples

```
$ python main.py "What organizations am I part of?"

The organizations you are part of are:
- microsoft
- github
- tensorflow
- kubernetes

$ python main.py "Show the latest commits from repository 'torvalds/linux'"

The latest commits in repository torvalds/linux are:
- commit abc123: Fix memory leak in scheduler
- commit def456: Update documentation
- commit ghi789: Add new driver support
```

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
