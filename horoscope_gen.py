from dotenv import load_dotenv
from openai import OpenAI
import os
import datetime

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 
def response_from_openai(horoscope, date):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": f"""
                   You give a 2 to 3 sentence horoscope for {date} and for {horoscope}.
                   make it in the following format:
                    date: {date}
                    horoscope: {horoscope}
                        (description).
                   """}],
    )
    return completion.choices[0].message.content



horoscope = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

date_unformated = datetime.datetime.now()
date = f"date: {date_unformated.day}/{date_unformated.month}/{date_unformated.year}"

file = open("./Horoskopa MI/horoscope.txt", "w")

for month in horoscope:
    file.write(response_from_openai(month, date))
    file.write("\n\n")
file.close()

    
