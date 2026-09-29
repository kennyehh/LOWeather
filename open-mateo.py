import urllib.request
import json


# Convert wind direction in degrees to a compass direction
def degrees_to_direction(degrees):
    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]

    index = round(degrees / 22.5) % 16
    return directions[index]

# Open-Meteo API request
url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=48.8378"
    "&longitude=-94.6977"
    "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_direction_10m,precipitation_probability"
    "&daily=precipitation_sum"
    "&past_days=5"
    "&temperature_unit=fahrenheit"
    "&wind_speed_unit=mph"
    "&precipitation_unit=inch"
)


# Request the data from Open-Meteo
with urllib.request.urlopen(url) as response:
    data = json.load(response)


# Get individual values from the returned data
temperature = data["current"]["temperature_2m"]
humidity = data["current"]["relative_humidity_2m"]
wind_speed = data["current"]["wind_speed_10m"]
wind_degrees = data["current"]["wind_direction_10m"]
precip_probability = data["current"]["precipitation_probability"]

# Convert wind degrees to compass direction
wind_direction = degrees_to_direction(wind_degrees)


# Display the weather
print("Current Weather at Wheeler's Point")
print("Temperature:", temperature, "°F")
print("Humidity:", humidity, "%")
print("Wind:", wind_direction,"-",wind_degrees, "°")
print("Wind Speed:", wind_speed, "mph")
print("Precipitation Probability",precip_probability, "%")

dates = data["daily"]["time"]
precipitation = data["daily"]["precipitation_sum"]

print("Past 5 Days Precipitation:")

for i in range(5):
    print(dates[i], precipitation[i], "in")
