# LOWeather

## LOWeather is a small app that will combine weather conditions from a specific location with current wave conditions on Lake of the Woods.

 - The current weather location is Wheeler's Point which is where the Rainy River meets the Lake of the Woods.
 - The current wave conditions come from a Wave Buoy located in the middle of Big Traverse Bay on Lake of the Woods.

## How it works

 - `app.py` - Flask web app that serves a single page (`/`)
 - `weather.py` - Gets current weather and past 5 days of precipitation from the [Open-Meteo API](https://open-meteo.com/) (no API key needed)
 - `buoy.py` - Gets the latest wave height and direction from the Obscape buoy portal (uses the API key in the file)
 - `templates/index.html` and `static/` - The page layout, styling and icon
 - `open-mateo.py` - Old standalone test script, not used by the app

### Requirements

 - Python packages: `flask` and `gunicorn` (listed in `requirements.txt`). Everything else uses the Python standard library.
 - The server needs outbound internet access to `api.open-meteo.com` and `obscape.com`.
 - The app runs on port **8090**.

## Installing with Docker (recommended)

These steps work on any Linux server. Other operating systems work too if Docker is installed.

### 1. Install Docker and Docker Compose

Follow the official instructions for your OS: https://docs.docker.com/engine/install/

Check that it's installed:

```bash
docker --version
docker compose version
```

(Optional) Let your user run Docker without `sudo`, then log out and back in:

```bash
sudo usermod -aG docker $USER
```

### 2. Get the code

```bash
git clone https://github.com/kennyehh/LOWeather.git
cd LOWeather
```

### 3. Build and start the app

```bash
docker compose up -d --build
```

 - `--build` builds the image from the `Dockerfile`
 - `-d` runs it in the background
 - `restart: unless-stopped` in `docker-compose.yml` makes it start again automatically after a reboot or crash

### 4. Check that it's running

```bash
docker compose ps
docker compose logs -f
```

Then open a browser to:

```
http://<server-ip>:8090
```

If the page doesn't load from another device, make sure port 8090 is open in the server's firewall. For example:

```bash
# Fedora / RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=8090/tcp
sudo firewall-cmd --reload

# Ubuntu / Debian (ufw)
sudo ufw allow 8090/tcp
```

### Updating to a new version

```bash
cd LOWeather
git pull
docker compose up -d --build
```

### Stopping / removing

```bash
docker compose down
```

### Changing the port

To use a different port on the host, change only the left side of the port mapping in `docker-compose.yml`. For example, to serve on port 80:

```yaml
    ports:
      - "80:8090"
```

Then run `docker compose up -d` again.

## Running without Docker (for testing)

Requires Python 3.

```bash
git clone https://github.com/kennyehh/LOWeather.git
cd LOWeather
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Run with the Flask development server (port 5000):

```bash
python app.py
```

Or run with gunicorn, the same way the Docker container does (port 8090, Linux/macOS only):

```bash
gunicorn --bind 0.0.0.0:8090 --workers 3 --timeout 60 app:app
```
