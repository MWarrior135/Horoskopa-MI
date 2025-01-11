import os
import requests
from aisetup import print_llm_response
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")
print(api_key)


