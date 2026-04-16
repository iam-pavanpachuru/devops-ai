## 👨‍💻 Author

**Pavan Kalyan Pachuru**

* GitHub: https://github.com/iam-pavanpachuru
* LinkedIn: https://www.linkedin.com/in/pavan-kalyan-pachuru-538a4016b

---

# 🚀 GitHub AI DevOps Agent (MCP + Gemini)

An AI-powered DevOps assistant that interacts with GitHub using natural language.

Built using:

* LangChain + LangGraph
* Google Gemini API
* Model Context Protocol (MCP)
* Custom GitHub tools

---

## ✨ Features

* 🧠 Supports natural language prompts (English)
* 📦 Create public/private repositories
* 🌿 Create branches
* 📄 Add README files
* 🔍 List branches & repository details
* 🗑️ Delete repositories (custom tool with safety confirmation)
* 🔁 Model fallback + retry logic
* 🔐 Safe execution (confirmation before destructive actions)

---

## 🏗️ Architecture

```
User Input
   ↓
AI Agent (LangGraph ReAct)
   ↓
Tools Layer
   ├── MCP GitHub Tools (via @modelcontextprotocol/server-github)
   └── Custom Tools (delete_repository)
   ↓
GitHub API
```

---

## ⚙️ Setup

## 🔑 Prerequisites

Before running this project, you need to generate the following:

### 1. Google Gemini API Key

* Go to: https://aistudio.google.com
* Sign in with your Google account
* Click **Get API Key** → **Create API key**
* Copy the key

---

### 2. GitHub Personal Access Token (PAT)

* Go to: https://github.com/settings/tokens
* Click **Generate new token (classic)**
* Select the following permissions:

  * ✅ `repo` (full control of repositories)
* Generate and copy the token

---

### 3. Your GitHub Username

* Your GitHub profile username
  Example:

  ```
  iam-pavanpachuru
  ```

---

## ⚙️ Configure Environment Variables

Update your `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
GITHUB_PERSONAL_ACCESS_TOKEN=your_github_token
GITHUB_USERNAME=your_username
```

---

⚠️ Never commit your `.env` file to GitHub. Add it to `.gitignore`.

---

### 1. Clone repo

```bash
git clone https://github.com/iam-pavanpachuru/github-ai-agent
cd github-ai-agent
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

Run the agent:

```bash
python github_ai_agent.py
```

Type your task and press **ENTER twice** to execute.

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