from dotenv import load_dotenv
from openai import OpenAI
from googletrans import Translator
import os
import datetime
import asyncio
import chardet


load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

#generate response to prompt
def response_from_openai(horoscope, date):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": f"""
                   You give a 2 to 5 sentence horoscope for {date} and for {horoscope}.
                   make it in the following format:
                    date: {date}
                    horoscope: {horoscope}
                        (description).
                   """}],
    )
    return completion.choices[0].message.content

#translate to latvian function
async def translate_file(en_file, lv_file):
    try:
        # Initialize the translator
        translator = Translator()
        
        with open(en_file, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            file_encoding = result['encoding']
        
        # Read the input file
        with open(en_file, 'r', encoding=file_encoding) as file:
            english_text = file.read()
        
        # Translate the text
        translated = await translator.translate(english_text, src='en', dest='lv')
        
        # Write the translated text to the output file
        with open(lv_file, 'w', encoding='utf-8') as file:
            file.write(translated.text)
        
        print(f"Translation completed. Translated text saved to {lv_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

###generation###
horoscope = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

date_unformated = datetime.datetime.now()
date = f"date: {date_unformated.day}/{date_unformated.month}/{date_unformated.year}"

en_file = f'./Horoskopa MI/horoscope{date_unformated.day}_{date_unformated.month}_{date_unformated.year}.txt'   # Replace with your input file path
lv_file = f'./Horoskopa MI/lv_horoscope{date_unformated.day}_{date_unformated.month}_{date_unformated.year}.txt' # Replace with your desired output file path

file = open(en_file, "w")

for month in horoscope:
    file.write(response_from_openai(month, date))
    file.write("\n\n")
file.close()
###generation###

###translation###

asyncio.run(translate_file(en_file, lv_file))
###translation###

    
