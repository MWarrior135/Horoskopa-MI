import swisseph as swe


# Load the Swiss Ephemeris data files
swe.set_ephe_path('D:\VS code projects\swisseph-master\ephe')  # Download from: https://www.astro.com/ftp/swisseph/

# Set the date for which you want to calculate the planetary positions
year, month, day = 2025, 1, 12

# Get planetary positions
def get_planet_positions(year, month, day):
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

    positions = {}
    for name, planet in planets.items():
        position, _ = swe.calc_ut(swe.julday(year, month, day), planet)
        zodiac_degree = position[0]  # Longitude in degrees
        #sign_index = int(zodiac_degree // 30)
        #sign = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"][sign_index]
        #degree_in_sign = zodiac_degree % 30
        #positions[name] = f"{degree_in_sign:.2f}° {sign}"
        positions[name] = zodiac_degree
        
    planet_position = {}
    # Output the planetary positions
    for planet, position in positions.items():
        planet_position[planet] = position
        #print(f"{planet}: {position}")
    print("planet locations extracted")
    return planet_position
    
print(get_planet_positions(year, month, day))
