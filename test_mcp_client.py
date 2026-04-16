from dotenv import load_dotenv
import os

load_dotenv()

print(os.getenv("GOOGLE_API_KEY")[:8])
print(os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")[:8])
print(os.getenv("GITHUB_USERNAME"))
