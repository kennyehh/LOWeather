from buoy import get_wave_data
from flask import Flask, render_template
from weather import get_weather_data

app = Flask(__name__)


@app.route("/")
def index():
    weather = get_weather_data()
    wave = get_wave_data()
    return render_template("index.html", weather=weather, wave=wave)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
