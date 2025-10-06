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
```

### How to get the keys:

1. **OpenAI API Key**: 
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create a new API key

2. **GitHub Token**:
   - Go to GitHub Settings > Developer settings > Personal access tokens
   - Generate a token with permissions to access repositories and organizations

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

3. Configure environment variables (see prerequisites section)

## 🎯 How to use

### Basic execution:
```bash
python main.py "Your question here"
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

### Interactive mode:
```bash
python main.py
# Type your question when prompted
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
