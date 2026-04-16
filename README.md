# 🚀 GitHub AI DevOps Agent (MCP + Gemini)

An AI-powered DevOps assistant that interacts with GitHub using natural language.

Built using:
- LangChain + LangGraph
- Google Gemini API
- Model Context Protocol (MCP)
- Custom GitHub tools

---

## ✨ Features

- 🧠 Supports natural language prompts (English)
- 📦 Create public/private repositories
- 🌿 Create branches
- 📄 Create/update files (README, etc.)
- 🔍 List repositories, branches, commits
- 🐛 Create issues & PRs
- 💬 Comment on issues
- 🗑️ Delete repositories (custom tool with safety confirmation)
- 🔁 Retry & fallback logic
- 🔐 Safe execution for destructive actions

---

## ✨ What This Project Does

Control GitHub like this:

```
"Create a branch named feat/aiagent-test in your repository (replace <reponame> with your repo name)"
```

Example:

```
Create a branch named feat/aiagent-test in ai-devops-demo
```

The agent will:
- Understand your intent
- Select the correct GitHub tool
- Execute it automatically

No GitHub API knowledge required.

---

## 🏗️ Architecture

```
User Input
   ↓
AI Agent (LangGraph ReAct)
   ↓
Tools Layer
   ├── MCP GitHub Server (@modelcontextprotocol/server-github)
   └── Custom Tools (delete_repository)
   ↓
GitHub API
```

---

# 🧑‍💻 One-Time Setup (New Laptop Friendly)

Follow these steps exactly — after this, the project will run without issues.

---

## 1️⃣ Install System Dependencies

### Install Python (>= 3.10)

```bash
python --version
```

If not installed → https://python.org

---

### Install Node.js (Required for MCP)

Download: https://nodejs.org

```bash
node -v
npm -v
```

---

### Install Git

```bash
git --version
```

---

## 2️⃣ Get Required Credentials

### Gemini API Key
- https://aistudio.google.com → Create API key

### GitHub Personal Access Token
Scopes required:
- repo
- workflow
- read:org

### GitHub Username

Example:
```
iam-pavanpachuru
```

---

## 3️⃣ Clone the Repository

```bash
git clone https://github.com/iam-pavanpachuru/github-ai-agent
cd github-ai-agent
```

---

## 4️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Linux / Mac
```bash
source venv/bin/activate
```

Windows
```bash
venv\\Scripts\\activate
```

---

## 5️⃣ Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 6️⃣ Setup MCP (Node Environment)

### Fix npm permissions (Linux/Mac)

```bash
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

### Install MCP Server

```bash
npm install -g @modelcontextprotocol/server-github
```

---

### Verify MCP Works

```bash
npx @modelcontextprotocol/server-github
```

Expected:
```
GitHub MCP Server running on stdio
```

---

## 7️⃣ Configure Environment Variables

Create `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
GITHUB_USERNAME=your_github_username  # e.g., iam-pavanpachuru
```

Protect it:

```bash
echo ".env" >> .gitignore
```

---

## 🔌 MCP Usage Modes (Important)

### ✅ Recommended — Auto Mode

- Python reads `.env`
- Passes token to MCP internally
- No manual setup required

---

### ⚙️ Manual Mode

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN=your_token
npx @modelcontextprotocol/server-github
```

---

## 🚀 Run the Project

```bash
python github_ai_agent.py
```

Type your task and press ENTER twice.

---

## 🧪 Validate Setup (Important)

Before running real tasks, verify everything is working correctly.

### 1. Validate Environment Variables

```bash
python test_mcp_client.py
```

Expected:
- MCP connects successfully
- GitHub authentication works

---

### 2. Validate MCP Tools

```bash
python inspect_mcp_tools.py
```

Expected:
- List of available GitHub tools
- Confirms MCP server is working

---

### 3. Quick Test Prompt

Run the agent and try:

```
List all repositories for my GitHub account
```

If this works → your setup is fully correct ✅

---

## 🧪 Example Prompts (MCP Tools)

Here are some example prompts demonstrating how the agent interacts with GitHub using MCP tools:

---

### 📦 Create Repository

```
Create a new private repository called ai-devops-demo
If empty, create a README.md with content "# AI DevOps"
```

---

### 📄 Create or Update File

```
Create a README.md file in ai-devops-demo with content "# AI DevOps Project"
```

---

### 🌿 Create Branch

```
Create a new branch called feat/auth in repository ai-devops-demo
```

---

### 🔍 Search Repositories

```
Search for repositories related to "devops automation"
```

---

### 🐛 Create Issue

```
Create an issue in ai-devops-demo with title "Bug: Fix login error" and description "Login fails on invalid credentials"
```

---

### 🔀 Create Pull Request

```
Create a pull request from branch feat/auth to main in ai-devops-demo with title "Add authentication feature"
```

---

### 💬 Add Comment to Issue

```
Add a comment to issue #1 in ai-devops-demo saying "Working on this issue"
```

---

### 🔎 List Commits

```
List all commits from the main branch in ai-devops-demo
```

---

### 🗑️ Delete Repository

```
Delete the repository ai-devops-demo
```

⚠️ Requires confirmation before execution.

---

## 🔧 Custom Tool: Delete Repository

The MCP GitHub server does **not support repository deletion**.

So we added a custom tool:

```python
def delete_github_repo(repo_name: str):
```

This directly calls GitHub REST API:

```
DELETE /repos/{owner}/{repo}
```

---

## 📁 Project Structure

```
.
├── github_ai_agent.py      # Main AI agent
├── inspect_mcp_tools.py   # Utility to inspect MCP tools
├── test_mcp_client.py     # MCP connection testing
├── .env                   # Environment variables
├── .gitignore
└── venv/
```

---

## 📌 File Explanations

### 🔹 github_ai_agent.py

Main application:

* Handles user input
* Connects to MCP server
* Loads tools
* Runs AI agent
* Executes GitHub operations

---

### 🔹 inspect_mcp_tools.py

**Purpose:** Tool discovery & debugging

Run:

```bash
python inspect_mcp_tools.py
```

Helps you:

* See all available MCP tools
* Understand system capabilities
* Debug why certain prompts fail

---

### 🔹 test_mcp_client.py

**Purpose:** Testing & validation

Used for:

* Verifying MCP connection
* Testing GitHub authentication
* Running quick experiments

---

## ⚠️ Known Limitations

* Gemini free tier has strict rate limits (429 errors)
* Some MCP tools may be missing (e.g., delete repo)
* Model availability may change (503 errors)

---

## 🧠 Key Learnings

* LLMs don’t execute actions — tools do
* MCP acts as a bridge between AI and real systems
* Safety checks are critical for destructive operations
* Prompt clarity improves tool usage

---

## 🔮 Future Improvements

* Will be updated with more features and enhancements soon 🚀

---

## 🤝 Contributing

Feel free to fork, improve, and share!

---

## ⭐ If you like this project

Give it a star ⭐ and share on LinkedIn 🚀

---

## 🙏 Acknowledgements

This project was built with the help of AI-assisted development tools, including ChatGPT, for guidance, debugging, and code suggestions.

---

## 👨‍💻 Author

Pavan Kalyan Pachuru

- GitHub: https://github.com/iam-pavanpachuru
- LinkedIn: https://www.linkedin.com/in/pavan-kalyan-pachuru-538a4016b