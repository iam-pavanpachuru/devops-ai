import asyncio
import os
import sys
import requests

# Toggle debug logs
DEBUG = True
if not DEBUG:
    sys.stderr = open(os.devnull, 'w')

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import Tool

# Load env
load_dotenv()

TOKEN = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

# =========================
# 🔧 CUSTOM DELETE TOOL
# =========================
def delete_github_repo(repo_name: str) -> str:
    """
    Deletes a GitHub repository for the authenticated user.
    """
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}"

    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.delete(url, headers=headers)

    if response.status_code == 204:
        return f"✅ Repository '{repo_name}' deleted successfully."
    elif response.status_code == 404:
        return f"❌ Repository '{repo_name}' not found."
    else:
        return f"❌ Failed to delete repo. Status: {response.status_code}, Response: {response.text}"

# Wrap as LangChain tool
delete_repo_tool = Tool(
    name="delete_repository",
    func=delete_github_repo,
    description="""
Delete a GitHub repository.

Input should be the repository name ONLY (not full URL).
Example:
ai-devops-private-repo
"""
)

# =========================
# 🧾 INPUT HANDLER
# =========================
def get_input():
    print("\n🤖 GitHub AI Agent")
    print("=" * 50)
    print(f"User : {USERNAME}")
    print("=" * 50)
    print("\nType your task. Press ENTER twice to execute\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    return "\n".join(lines)


# =========================
# 🚀 MAIN RUNNER
# =========================
async def run(task: str):

    # 🔐 Safety check for delete
    if "delete" in task.lower():
        confirm = input("⚠️ Are you sure you want to delete? (yes/no): ")
        if confirm.lower() != "yes":
            print("❌ Operation cancelled")
            return

    # MCP GitHub tools
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": TOKEN
                },
                "transport": "stdio"
            }
        }
    )

    mcp_tools = await client.get_tools()

    # ➕ Combine MCP + custom tool
    tools = mcp_tools + [delete_repo_tool]

    print(f"\n✅ GitHub MCP connected — {len(mcp_tools)} tools")
    print(f"➕ Custom tools loaded — 1 (delete_repository)\n")

    # 🔁 Model fallback
    models = [
        "gemini-3.1-flash-lite-preview",
        "gemini-2.5-flash"
    ]

    for model_name in models:
        print(f"\n🚀 Trying model: {model_name}")

        llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0,
            max_retries=2,
            request_timeout=60
        )

        agent = create_react_agent(llm, tools)

        for attempt in range(3):
            try:
                result = await agent.ainvoke({
                    "messages": [
                        {
                            "role": "user",
                            "content": f"""
You are a Senior DevOps engineer.

GitHub username: {USERNAME}

Rules:
- Use available tools when needed
- If deleting a repo, call delete_repository tool
- Be precise and safe

Task:
{task}
"""
                        }
                    ]
                })

                final = result["messages"][-1].content

                print("\n" + "=" * 50)
                print("✅ RESULT")
                print("=" * 50)
                print(final)
                return

            except Exception as e:
                print(f"\n⚠️ Attempt {attempt + 1} failed")

                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    print("🔥 Gemini overloaded, retrying...")
                elif "429" in str(e):
                    print("⚠️ Rate limit hit. Try later.")
                else:
                    print(f"Error: {str(e)}")

                if attempt < 2:
                    print("⏳ Retrying in 3 seconds...")
                    await asyncio.sleep(3)
                else:
                    print("❌ Max retries reached for this model")

        print(f"❌ Model {model_name} failed, trying next...\n")

    print("\n❌ All models failed. Try again later.")


# =========================
# 🏁 ENTRY POINT
# =========================
if __name__ == "__main__":
    task = get_input()
    print("\n👉 Running task...\n")
    asyncio.run(run(task))