# GitHub Code Assistant

An intelligent assistant that connects OpenAI's GPT with GitHub through the Model Context Protocol (MCP). Ask natural questions about your repositories, pull requests, issues, and get actionable insights.

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export OPENAI_API_KEY="your_openai_key_here"
export GITHUB_TOKEN="your_github_token_here"
export GITHUB_LOGIN="your_github_username"
```

3. **Run the assistant:**
```bash
python main.py
```

## Usage Examples

### Pull Request Management
```
User: Which PRs could use my attention?

Assistant: Thinking ...
Assistant: Here are the PRs that could use your attention:

**Your open PRs:**
1) company/web-app #142 — "Add user authentication"
   - Link: https://github.com/company/web-app/pull/142
   - Status: Ready for review

2) company/api #89 — "Refactor database queries"
   - Link: https://github.com/company/api/pull/89
   - Status: CI pending

If you'd like, I can: request a Copilot review, fetch reviewers details, or trigger CI runs.

User: I want a Copilot review

Assistant: Thinking ...

Assistant: Copilot review requested for your PRs:

1) company/web-app #142 — "Add user authentication"
   - Link: https://github.com/company/web-app/pull/142
   - Status: Copilot review requested

2) company/api #89 — "Refactor database queries"
   - Link: https://github.com/company/api/pull/89
   - Status: Copilot review requested

Would you like me to check back for feedback once it's posted?
```

### Repository Insights
```
User: What's the health status of my main repositories?

Assistant: Here's the health overview of your repositories:

**Active Development:**
- company/core-api: 12 open PRs, 3 failing CI, 8 pending reviews
- company/frontend: 5 open PRs, all CI passing, needs dependency updates

**Needs Attention:**
- company/legacy-system: 23 open issues, 5 critical bugs, no recent activity
- company/docs: 7 outdated pages, last updated 2 months ago

**Recommendations:**
- Prioritize critical bugs in legacy-system
- Update dependencies in frontend (3 major versions behind)
- Schedule docs review session
```

### Issue Tracking
```
User: What critical issues should I tackle this week?

Assistant: Here are the critical issues requiring immediate attention:

**High Priority (P0):**
1) company/api #234 - "Database connection pool exhaustion"
   - Link: https://github.com/company/api/issues/234

2) company/frontend #189 - "Memory leak in dashboard"
   - Link: https://github.com/company/frontend/issues/189

**Medium Priority (P1):**
3) company/mobile #156 - "Push notifications not working on iOS"
   - Link: https://github.com/company/mobile/issues/156
```

## Prerequisites

- **Docker** (for MCP GitHub server)
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
- **GitHub Personal Access Token** ([Generate here](https://github.com/settings/tokens))
