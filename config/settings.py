import os
from dotenv import load_dotenv
from pathlib import Path

current_dir = Path(__file__).resolve().parent
load_dotenv(current_dir / '.env')

API_KEY = os.getenv("API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SCRAP_API_KEY = os.getenv("SCRAP_API_KEY")
REDIS = os.getenv("REDIS", 'redis://localhost:6379/0')
TRACE_AI = os.getenv("TRACE_AI", 'false') == 'true'
BRAVE_SEARCH_API_KEY = os.getenv("BRAVE_SEARCH_API_KEY")
API_URL = os.getenv("API_URL", "http://localhost:8000")
