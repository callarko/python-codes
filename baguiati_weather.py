#!/usr/bin/env python3
"""Show current weather for the laptop's location or Baguiati, Kolkata.

This program uses only Python's standard library. It opens a local browser page
so the browser can request location permission, then queries Open-Meteo using
the resulting coordinates. No coordinates are saved or sent anywhere else.
"""

from __future__ import annotations

import json
import ssl
import subprocess
import threading
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


HOST = "127.0.0.1"
PORT = 8765

# Approximate centre of Baguiati, Kolkata 700059. Device location is preferred.
BAGUIATI = {"latitude": 22.6138, "longitude": 88.4300, "accuracy": None}

WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def get_weather(latitude: float, longitude: float) -> dict:
    current_fields = (
        "temperature_2m,relative_humidity_2m,apparent_temperature,"
        "precipitation,rain,showers,weather_code,cloud_cover,"
        "surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
    )
    params = urllib.parse.urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": current_fields,
            "timezone": "Asia/Kolkata",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
            "forecast_days": 1,
        }
    )
    request = urllib.request.Request(
        f"https://api.open-meteo.com/v1/forecast?{params}",
        headers={"User-Agent": "BaguiatiWeather/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.load(response)
    except urllib.error.URLError as exc:
        # Some python.org macOS installations have no CA bundle configured.
        # Use the system curl certificate store; never disable TLS verification.
        if not isinstance(exc.reason, ssl.SSLCertVerificationError):
            raise
        completed = subprocess.run(
            ["curl", "--fail", "--silent", "--show-error", "--max-time", "15", request.full_url],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)


def result_payload(location: dict) -> dict:
    latitude = float(location["latitude"])
    longitude = float(location["longitude"])
    data = get_weather(latitude, longitude)
    current = data["current"]
    units = data["current_units"]
    code = int(current["weather_code"])
    return {
        "condition": WEATHER_CODES.get(code, f"Weather code {code}"),
        "observed_at": current["time"],
        "latitude": latitude,
        "longitude": longitude,
        "accuracy_m": location.get("accuracy"),
        "weather_grid_latitude": data["latitude"],
        "weather_grid_longitude": data["longitude"],
        "temperature": f'{current["temperature_2m"]}{units["temperature_2m"]}',
        "feels_like": f'{current["apparent_temperature"]}{units["apparent_temperature"]}',
        "humidity": f'{current["relative_humidity_2m"]}{units["relative_humidity_2m"]}',
        "precipitation": f'{current["precipitation"]} {units["precipitation"]}',
        "rain": f'{current["rain"]} {units["rain"]}',
        "cloud_cover": f'{current["cloud_cover"]}{units["cloud_cover"]}',
        "pressure": f'{current["surface_pressure"]} {units["surface_pressure"]}',
        "wind": f'{current["wind_speed_10m"]} {units["wind_speed_10m"]}',
        "wind_direction": f'{current["wind_direction_10m"]}{units["wind_direction_10m"]}',
        "wind_gusts": f'{current["wind_gusts_10m"]} {units["wind_gusts_10m"]}',
    }


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Baguiati Weather</title><style>
body{font:16px system-ui;max-width:680px;margin:3rem auto;padding:0 1rem;color:#18212b}
button{padding:.75rem 1rem;margin:.4rem;border:0;border-radius:.5rem;background:#1267d6;color:white;font-weight:600}
.secondary{background:#59636e} .card{background:#f3f6f9;padding:1rem 1.4rem;border-radius:1rem;margin-top:1rem}
dt{font-weight:650} dd{margin:0 0 .65rem} small{color:#59636e}
</style></head><body>
<h1>Local weather</h1>
<p>Use the laptop's location for the closest available weather grid, or use Baguiati 700059.</p>
<button onclick="locate()">Use my laptop location</button>
<button class="secondary" onclick="send(%(lat)s,%(lon)s,null)">Use Baguiati fallback</button>
<p id="status"><small>Location is shared only with this Python program on your laptop.</small></p>
<div id="result"></div>
<script>
const status=document.getElementById('status'), result=document.getElementById('result');
function locate(){
 status.textContent='Waiting for location permission…';
 if(!navigator.geolocation){status.textContent='Geolocation is unavailable; use the fallback.';return;}
 navigator.geolocation.getCurrentPosition(
  p=>send(p.coords.latitude,p.coords.longitude,p.coords.accuracy),
  e=>status.textContent='Location unavailable: '+e.message+'. You can use the Baguiati fallback.',
  {enableHighAccuracy:true,timeout:15000,maximumAge:60000});
}
async function send(latitude,longitude,accuracy){
 status.textContent='Fetching current weather…'; result.innerHTML='';
 try{
  const response=await fetch('/weather',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({latitude,longitude,accuracy})});
  const data=await response.json(); if(!response.ok) throw new Error(data.error);
  status.textContent='';
  result.innerHTML='<div class="card"><h2>'+data.condition+'</h2><dl>'+[
   ['Temperature',data.temperature],['Feels like',data.feels_like],['Humidity',data.humidity],
   ['Rain',data.rain],['Cloud cover',data.cloud_cover],['Wind',data.wind],
   ['Wind gusts',data.wind_gusts],['Surface pressure',data.pressure],['Weather time',data.observed_at]
  ].map(x=>'<dt>'+x[0]+'</dt><dd>'+x[1]+'</dd>').join('')+'</dl><small>Coordinates: '+
  data.latitude.toFixed(5)+', '+data.longitude.toFixed(5)+(data.accuracy_m?' (device accuracy about '+
  Math.round(data.accuracy_m)+' m)':' (Baguiati fallback)')+'</small></div>';
 }catch(e){status.textContent='Could not fetch weather: '+e.message;}
}
</script></body></html>""" % {"lat": BAGUIATI["latitude"], "lon": BAGUIATI["longitude"]}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/":
            self.send_error(404)
            return
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        if self.path != "/weather":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            location = json.loads(self.rfile.read(length))
            latitude = float(location["latitude"])
            longitude = float(location["longitude"])
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                raise ValueError("Invalid coordinates")
            payload, status = result_payload(location), 200
            print_weather(payload)
        except (
            KeyError,
            ValueError,
            json.JSONDecodeError,
            urllib.error.URLError,
            subprocess.SubprocessError,
        ) as exc:
            payload, status = {"error": str(exc)}, 400
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, _format: str, *_args: object) -> None:
        return


def print_weather(data: dict) -> None:
    print("\nCurrent weather")
    print(f'  Condition:   {data["condition"]}')
    print(f'  Temperature: {data["temperature"]} (feels like {data["feels_like"]})')
    print(f'  Humidity:    {data["humidity"]}')
    print(f'  Rain:        {data["rain"]}')
    print(f'  Cloud cover: {data["cloud_cover"]}')
    print(f'  Wind:        {data["wind"]}, gusts {data["wind_gusts"]}')
    print(f'  Updated:     {data["observed_at"]} Asia/Kolkata')


def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    url = f"http://{HOST}:{PORT}/"
    print(f"Opening {url}")
    print("Allow location access in the browser, or choose the Baguiati fallback.")
    print("Press Ctrl+C here when finished.")
    threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWeather server stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
