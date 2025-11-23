from countryCodes import get_country_by_code, country_codes
import requests
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

class GeoInfo:

  def __init__(self, city):
    self._api_key = "YOUR_API_KEY_HERE"
    self.city = city
    self.geo_json = self.get_geo_json()
    
    
    
  def get_geo_json(self):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={self.city}&limit=1&appid={self._api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
      print(f"Error in recieving response for getting geo JSON: status code {response.status_code}")
      return None
    elif not response.json():
      print("Empty JSON")
      return None
    else:
      return response.json()
    
    
    
  def fetch_latitude(self):
      if self.geo_json:
          return self.geo_json[0].get("lat")

  
  def fetch_longitude(self):
      if self.geo_json:
          return self.geo_json[0].get("lon")
    
  def fetch_country(self):
      if self.geo_json:
          code = self.geo_json[0].get("country")
          return get_country_by_code(code)
  
  def fetch_city(self):
      if self.geo_json:
          return self.geo_json[0].get("name")
        
        
        
  def fetch_state(self):
      """Use reverse geocoding to get state from lat/lon, quietly on failure"""
      lat = self.fetch_latitude()
      lon = self.fetch_longitude()
      if lat is None or lon is None:
          return "N/A"

      geolocator = Nominatim(user_agent="city_to_state_app")
      try:
          location = geolocator.reverse((lat, lon), exactly_one=True, language="en", timeout=5)
          if location and location.raw and 'address' in location.raw:
              return location.raw['address'].get('state', 'N/A')
          return "N/A"
      except Exception:
          # Hide all geocoding errors (e.g., timeout, connection error, rate limit)
          return "N/A"


  


    
    

  
