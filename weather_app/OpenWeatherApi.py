from geoCode import GeoInfo
import requests

class WeatherInfo:
    def __init__(self, city):
        self._api_key = "d1567f53e1833fe1fd68683da7d1e00d"
        self.units = "imperial"
        self.error_message = None

        # Initialize GeoInfo safely
        self.geo = GeoInfo(city)
        if not self.geo.geo_json:
            self.error_message = f"Couldn't find location data for '{city}'."
            self.weather_json = None
            return

        self.latitude = self.geo.fetch_latitude()
        self.longitude = self.geo.fetch_longitude()
        self.city = self.geo.fetch_city()
        self.country = self.geo.fetch_country()
        self.state = self.geo.fetch_state()
        self.weather_json = self.get_weather_json()

    def get_weather_json(self):
        """Fetch weather data safely"""
        if not self.latitude or not self.longitude:
            self.error_message = "Missing latitude or longitude for weather lookup."
            return None
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.longitude}&appid={self._api_key}&units={self.units}"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                self.error_message = f"Weather API error: Status code {response.status_code}"
                return None

            data = response.json()
            if not data:
                self.error_message = "Empty weather data received."
                return None
            return data
        except requests.exceptions.RequestException as e:
            self.error_message = f"Network error fetching weather data: {e}"
            return None

    # -------- Data Getters --------
    def get_temp(self):
        try:
            return round(self.weather_json["main"]["temp"])
        except Exception:
            return None

    def get_humidity(self):
        try:
            return self.weather_json["main"]["humidity"]
        except Exception:
            return None

    def get_description(self):
        try:
            return self.weather_json["weather"][0]["description"]
        except Exception:
            return None

    def get_feels_like(self):
        try:
            return round(self.weather_json["main"]["feels_like"])
        except Exception:
            return None

    def get_wind_speed(self):
        try:
            return round(self.weather_json["wind"].get("speed", 0))
        except Exception:
            return None

    def get_precipitation_chance(self):
        """Fetch precipitation forecast percentage"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={self.latitude}&lon={self.longitude}&appid={self._api_key}&units={self.units}"
            response = requests.get(url, timeout=10)
            data = response.json()
            if "list" in data and data["list"]:
                return f"{round(data['list'][0].get('pop', 0) * 100)}%"
            return "N/A"
        except Exception:
            return "N/A"
