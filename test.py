import os
import requests

print(os.environ.get('NASA_KEY'))
# Your NASA API key (replace with your actual key)
api_key = os.environ.get('NASA_KEY')


def get_planetary_positions(date, target="Earth"):
    """
    Get the planetary position for a given date.
    :param date: The date to query the planetary position for (format: YYYY-MM-DD)
    :param target: The target planet or celestial object. Default is "Earth".
    :return: JSON data containing planetary positions.
    """
    # Horizon's API endpoint
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    
    # Parameters for the API call
    params = {
        "format": "json",  # Format the response as JSON
        "target": target,  # Target object (e.g., "Earth", "Mars", etc.)
        "time_span": "1",  # Time span: 1 day
        "time": date,      # The specific date for the planetary position
    }
    
    # Make the request to NASA Horizons API
    response = requests.get(url, params=params)

    # Check if the response was successful
    if response.status_code == 200:
        return response.json()  # Return the response data as JSON
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage:
date = "2025-01-12"
planet_positions = get_planetary_positions(date)

if planet_positions:
    print("Planetary Positions:")
    print(planet_positions)