import os
from dotenv import load_dotenv
#from openai import OpenAI
import datetime
load_dotenv()

x = datetime.datetime.now()
print(f"date: {x.day}/{x.month}/{x.year}")