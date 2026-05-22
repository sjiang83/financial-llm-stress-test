import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("QWEN_API_KEY")
model = os.getenv("QWEN_MODEL")
base_url = os.getenv("QWEN_BASE_URL")

print("QWEN_API_KEY exists:", key is not None)
print("QWEN_API_KEY length:", len(key) if key else 0)
print("QWEN_MODEL:", model)
print("QWEN_BASE_URL:", base_url)
