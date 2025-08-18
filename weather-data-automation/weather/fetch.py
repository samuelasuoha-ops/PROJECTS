import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_weather(latitude: float, longitude: float, hours_back: int = 72):
    past_days = max(1, min(7, (hours_back + 23) // 24))
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,precipitation",
        "timezone": "UTC",
        "past_days": past_days
    }
    r = requests.get(OPEN_METEO_URL, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return parse_open_meteo(data)

def parse_open_meteo(data: dict):
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    hums  = hourly.get("relative_humidity_2m", [])
    precs = hourly.get("precipitation", [])
    rows = []
    for i, ts in enumerate(times):
        try:
            rows.append({
                "ts_utc": ts,
                "temperature_c": float(temps[i]) if i < len(temps) else None,
                "relative_humidity": float(hums[i]) if i < len(hums) else None,
                "precipitation_mm": float(precs[i]) if i < len(precs) else None,
            })
        except Exception:
            continue
    return rows
