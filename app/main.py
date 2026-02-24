import os
import sys
import requests


def get_weather() -> None:
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("ERROR: API_KEY environment variable is not set", file=sys.stderr) # noqa501
        sys.exit(1)

    url = "https://api.weatherapi.com/v1/current.json"
    params = {"key": api_key, "q": "Paris", "aqi": "no"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"ERROR: request failed: {e}", file=sys.stderr)
        # полезно показать текст ответа, если он есть
        if "response" in locals() and response is not None:
            try:
                print(response.text, file=sys.stderr)
            except Exception:
                pass
        sys.exit(1)
    except ValueError:
        print("ERROR: response is not valid JSON", file=sys.stderr)
        sys.exit(1)

    location = data.get("location", {})
    current = data.get("current", {})
    condition = (current.get("condition") or {}).get("text")

    city = location.get("name", "Paris")
    country = location.get("country", "")
    temp_c = current.get("temp_c")
    feelslike_c = current.get("feelslike_c")
    wind_kph = current.get("wind_kph")
    humidity = current.get("humidity")

    print(f"City: {city}" + (f", {country}" if country else ""))
    print(f"Condition: {condition}")
    print(f"Temperature (C): {temp_c}")
    print(f"Feels like (C): {feelslike_c}")
    print(f"Wind (kph): {wind_kph}")
    print(f"Humidity (%): {humidity}")


if __name__ == "__main__":
    get_weather()
