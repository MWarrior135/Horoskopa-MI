from dotenv import load_dotenv
from openai import OpenAI
from googletrans import Translator
from datetime import datetime
import swisseph as swe
import os
import json
import asyncio
import chardet

#Have the chosen one non-comented
date = datetime.now() #takes todays date
#date = datetime(2014, 12, 23) #takes chosen date, format year, month, day

#loads api key from .env file
load_dotenv()

#loads zodiac_personalities from json file
with open('Horoskopa MI\zodiac_personalities.json', 'r') as file:
    zodiac_personalities = json.load(file)
    
#sets the path to the ephemeris file, needed in getting planet positions
swe.set_ephe_path('D:\VS code projects\Horoskopa MI\swisseph-master\ephe') #moved it right before cleaning up the file

#opens the connection to the openai api
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY")) 

# Function to get the response from OpenAI
def response_from_openai(horoscope, prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[{"role": "user", "content": prompt}],
    )
    print(horoscope, "done.")
    return completion.choices[0].message.content

def get_planet_positions(date):
    planets = {
        "Sun": swe.SUN,
        "Moon": swe.MOON,
        "Mercury": swe.MERCURY,
        "Venus": swe.VENUS,
        "Mars": swe.MARS,
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Uranus": swe.URANUS,
        "Neptune": swe.NEPTUNE,
        "Pluto": swe.PLUTO
    }

    planet_positions = {}
    jd = swe.julday(date.year, date.month, date.day, 12.0, 1)  # Julian day calculation

    for name, planet in planets.items():
        position, _ = swe.calc_ut(jd, planet)  # Calculate planetary position
        longitude = position[0]  # Longitude in degrees
        latitude = position[1]   # Latitude in degrees
        planet_positions[name] = {
            "longitude": longitude,
            "latitude": latitude
        }
    #print(planet_positions)
    #print("Planet locations extracted.")
    return planet_positions

# Function to calculate house placements
def calculate_house_positions(date, planet_positions):
    jd = swe.julday(date.year, date.month, date.day, 12.0, 1)  # Julian day calculation
    
    cusps, ascmc = swe.houses(jd, 56.9496, 24.1052, b'w')  # Calculate house cusps (Placidus house system) location is Riga

    house_positions = {}
    for planet, data in planet_positions.items():
        longitude = data["longitude"]
        # Determine the house for the planet based on its longitude
        house = next((i + 1 for i, cusp in enumerate(cusps[:-1]) if cusp <= longitude < cusps[i + 1]), 12)
        house_positions[planet] = house  # Store the house number for the planet

    #print(house_positions)
    #print("House positions calculated.")
    return house_positions

# Function to generate horoscope prompt based on date and planetary data
def generate_prompt(date, house_positions, zodiac_sign):

    #print("test")
    prompt = f"""
    House Positions:
    Sun: House {house_positions['Sun']}, 
    Moon: House {house_positions['Moon']}, 
    Mercury: House {house_positions['Mercury']}, 
    Venus: House {house_positions['Venus']}, 
    Mars: House {house_positions['Mars']}, 
    Jupiter: House {house_positions['Jupiter']}, 
    Saturn: House {house_positions['Saturn']}, 
    Uranus: House {house_positions['Uranus']}, 
    Neptune: House {house_positions['Neptune']}, 
    Pluto: House {house_positions['Pluto']}

    Astrological Houses:
    1: Self, Appearance, First Impressions, Beginnings
    2: Values, Possessions, Money, Self-Worth
    3: Communication, Siblings, Local Travel, Learning
    4: Home, Family, Roots, Emotional Foundation
    5: Creativity, Romance, Fun, Children
    6: Work, Health, Daily Routines, Service
    7: Partnerships, Marriage, Close Relationships
    8: Transformation, Shared Resources, Intimacy, Death/Rebirth
    9: Philosophy, Higher Learning, Travel, Beliefs
    10: Career, Reputation, Public Image, Goals
    11: Friendships, Community, Aspirations, Social Causes
    12: Subconscious, Secrets, Solitude, Spirituality

    Zodiac Sign: {zodiac_sign}
    - Element: {zodiac_personalities[zodiac_sign]['element']}
    - Modality: {zodiac_personalities[zodiac_sign]['modality']}
    - Personality Traits: {zodiac_personalities[zodiac_sign]['personality']}

    Prompt Details:
    - Interpret the impact of the house placements specifically for {zodiac_sign}, considering its element ({zodiac_personalities[zodiac_sign]['element']}) and modality ({zodiac_personalities[zodiac_sign]['modality']}).
    - Use the personality traits of {zodiac_sign} to craft a horoscope tailored to individuals with this zodiac sign.
    - Incorporate how the planetary alignments and house positions influence the key traits and challenges for {zodiac_sign} during this time.

    Generate a short horoscope for {zodiac_sign}, in 2 to 3 sentences, make the description simple and short. don't mention houses or planets, just the horoscope. format it as a text file, with UTF-8 encoding, with this structure and nothing else.:
        date: {date.year}/{date.month}/{date.day}
        horoscope: {zodiac_sign}
        (description).
    """
    return prompt

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

horoscope = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]


en_file = f'./Horoskopa MI/Archive/horoscope{date.day}_{date.month}_{date.year}.txt'   # Replace with your input file path
lv_file = f'./Horoskopa MI/Archive/lv_horoscope{date.day}_{date.month}_{date.year}.txt' # Replace with your desired output file path

file = open(en_file, "w")
for zodiac in horoscope:
    prompt = generate_prompt(date, calculate_house_positions(date, get_planet_positions(date)), zodiac)
    file.write(response_from_openai(zodiac, prompt))
    file.write("\n\n")
file.close()

asyncio.run(translate_file(en_file, lv_file))


    
