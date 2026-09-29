import json
import urllib.error
import urllib.request

WHEELERS_POINT_LATITUDE = 48.8378
WHEELERS_POINT_LONGITUDE = -94.6977
REQUEST_TIMEOUT_SECONDS = 10


# Convert direction in degrees to a compass direction
def degrees_to_direction(degrees):
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]

    index = round(degrees / 22.5) % 16
    return directions[index]


def get_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={WHEELERS_POINT_LATITUDE}"
        f"&longitude={WHEELERS_POINT_LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m,visibility,precipitation_probability"
        "&daily=precipitation_sum"
        "&past_days=5"
        "&forecast_days=1"
        "&temperature_unit=fahrenheit"
        "&wind_speed_unit=mph"
        "&precipitation_unit=inch"
    )

    try:
        with urllib.request.urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            data = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None

    current = data["current"]
    wind_degrees = current["wind_direction_10m"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "wind_gusts": current["wind_gusts_10m"],
        "wind_degrees": wind_degrees,
        "wind_direction": degrees_to_direction(wind_degrees),
        "visibility": round(current["visibility"] / 1609.34, 1),
        "precip_probability": current["precipitation_probability"],
        "past_precip": list(zip(
            data["daily"]["time"][:-1],
            data["daily"]["precipitation_sum"][:-1],
        )),
    }
