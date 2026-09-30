import json
import urllib.error
import urllib.request
from datetime import datetime

WHEELERS_POINT_LATITUDE = 48.8378
WHEELERS_POINT_LONGITUDE = -94.6977
TIMEZONE = "America/Chicago"
REQUEST_TIMEOUT_SECONDS = 10
PAST_DAYS = 5
FORECAST_DAYS = 5
HOURLY_HOURS = 12


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


# "2026-09-29T19:01" -> "7:01 PM"
def format_clock(timestamp):
    return datetime.fromisoformat(timestamp).strftime("%I:%M %p").lstrip("0")


# "2026-09-29T20:00" -> "8 PM"
def format_hour(timestamp):
    return datetime.fromisoformat(timestamp).strftime("%I %p").lstrip("0")


# "2026-09-29" -> "Tue 9/29"
def format_day(date):
    day = datetime.fromisoformat(date)
    return f"{day.strftime('%a')} {day.month}/{day.day}"


def get_weather_data():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={WHEELERS_POINT_LATITUDE}"
        f"&longitude={WHEELERS_POINT_LONGITUDE}"
        "&current=temperature_2m,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation_probability"
        "&hourly=temperature_2m,precipitation,precipitation_probability,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        "&daily=precipitation_sum,temperature_2m_max,temperature_2m_min,sunrise,sunset,"
        "precipitation_probability_max,precipitation_hours,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant"
        f"&past_days={PAST_DAYS}"
        f"&forecast_days={FORECAST_DAYS}"
        f"&timezone={TIMEZONE}"
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
    hourly = data["hourly"]
    daily = data["daily"]
    wind_degrees = current["wind_direction_10m"]

    # Daily lists hold the past days first, then today and the forecast days
    past_precip = [
        (format_day(daily["time"][i]), daily["precipitation_sum"][i])
        for i in range(PAST_DAYS)
    ]

    forecast = []
    for i in range(PAST_DAYS, PAST_DAYS + FORECAST_DAYS):
        forecast.append({
            "day": "Today" if i == PAST_DAYS else format_day(daily["time"][i]),
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "sunrise": format_clock(daily["sunrise"][i]),
            "sunset": format_clock(daily["sunset"][i]),
            "precip_probability_max": daily["precipitation_probability_max"][i],
            "precip_hours": daily["precipitation_hours"][i],
            "wind_speed_max": daily["wind_speed_10m_max"][i],
            "wind_gusts_max": daily["wind_gusts_10m_max"][i],
            "wind_degrees": daily["wind_direction_10m_dominant"][i],
            "wind_direction": degrees_to_direction(daily["wind_direction_10m_dominant"][i]),
        })

    # Start the hourly forecast at the current hour
    current_hour = current["time"][:13] + ":00"
    start = hourly["time"].index(current_hour) if current_hour in hourly["time"] else 0

    hours = []
    for i in range(start, min(start + HOURLY_HOURS, len(hourly["time"]))):
        hours.append({
            "hour": format_hour(hourly["time"][i]),
            "temperature": hourly["temperature_2m"][i],
            "precipitation": hourly["precipitation"][i],
            "precip_probability": hourly["precipitation_probability"][i],
            "wind_speed": hourly["wind_speed_10m"][i],
            "wind_gusts": hourly["wind_gusts_10m"][i],
            "wind_degrees": hourly["wind_direction_10m"][i],
            "wind_direction": degrees_to_direction(hourly["wind_direction_10m"][i]),
        })

    return {
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"],
        "wind_gusts": current["wind_gusts_10m"],
        "wind_degrees": wind_degrees,
        "wind_direction": degrees_to_direction(wind_degrees),
        "precip_probability": current["precipitation_probability"],
        "sunrise": forecast[0]["sunrise"],
        "sunset": forecast[0]["sunset"],
        "past_precip": past_precip,
        "hourly": hours,
        "forecast": forecast,
    }
