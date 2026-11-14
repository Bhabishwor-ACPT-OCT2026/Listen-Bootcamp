import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

print("OpenAI key loaded:", bool(os.getenv("OPENAI_API_KEY")))
