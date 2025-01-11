import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
#assign api keys to variables
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
weather_api_key = os.environ.get("WEATHER_API_KEY")

def response_from_openai(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": f"give a pointed answer, to this prompt: {prompt}"}],
    )
    return completion.choices[0].message.content


# Store the latitude and longtitude value in the 'lat' nad 'lon' variable
lat = 23.527281   
lon = -109.957152
weather_url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt=1&lat={lat}&lon={lon}&appid={weather_api_key}"

weather_response = requests.get(weather_url)
data = weather_response.json()
temperature = data['list'][0]['main']['temp']
description = data['list'][0]['weather'][0]['description']
wind_speed = data['list'][0]['wind']['speed']

weather_string = f"""The temperature is {temperature}°C. 
It is currently {description},
with a wind speed of {wind_speed}m/s.
"""
print(weather_string, "\n")
prompt = f"""Based on the following weather, 
suggest an appropriate outdoor outfit.

Forecast: {weather_string}
"""
response = response_from_openai(prompt)
print(response)
