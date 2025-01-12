import os
import asyncio
import chardet
from googletrans import Translator

async def translate_file(input_file, output_file):
    try:
        # Initialize the translator
        translator = Translator()
        
        with open(input_file, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            file_encoding = result['encoding']
        
        # Read the input file
        with open(input_file, 'r', encoding=file_encoding) as file:
            english_text = file.read()
        
        # Translate the text
        translated = await translator.translate(english_text, src='en', dest='lv')
        
        # Write the translated text to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(translated.text)
        
        print(f"Translation completed. Translated text saved to {output_file}.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the async function
input_file = './Horoskopa MI/horoscope.txt'   # Replace with your input file path
output_file = './Horoskopa MI/lv_horoscope.txt' # Replace with your desired output file path
asyncio.run(translate_file(input_file, output_file))

