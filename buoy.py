import json
import re
import urllib.error
import urllib.request

OBSCAPE_API_KEY = "H9pd6E2TsnewBFvgybSNjrPtLXf7qmCRuJ85WMZkUcQYx4ah3K"
REQUEST_TIMEOUT_SECONDS = 10


# Convert degrees to a 16-point compass direction
def degrees_to_direction(degrees):
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]

    index = round(degrees / 22.5) % 16
    return directions[index]


def get_wave_data():

    url = f"https://obscape.com/portal/graphapi/v1/api?key={OBSCAPE_API_KEY}"

    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            html = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError):
        return None

    # Find the JSON data embedded in the HTML
    match = re.search(r"var data = (\[.*?\]);", html, re.DOTALL)

    if not match:
        return None

    try:
        data = json.loads(match.group(1))

        # Get newest wave height and direction readings
        latest_wave = data[0]["data"][-1]
        latest_direction = data[1]["data"][-1]

        wave_height = latest_wave["Hmax"]
        wave_degrees = latest_direction["Dirm"]
    except (json.JSONDecodeError, IndexError, KeyError):
        return None

    wave_direction = degrees_to_direction(wave_degrees)

    # Send the results back to weather.py
    return {
        "height": wave_height,
        "degrees": wave_degrees,
        "direction": wave_direction,
        "time": latest_wave["tstr"]
    }
