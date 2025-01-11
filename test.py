import os
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);



 
#get AI API key
#Rewatch python tutorial about jupiter notebook