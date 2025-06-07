```python
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAPI:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.api_key = os.getenv('OPENWEATHER_API_KEY', self.config['api']['api_key'])
        self.base_url = self.config['api']['openweather_url']
        self.forecast_url = self.config['api']['forecast_url']
        
    def get_current_weather(self, city: str = None, lat: float = None, lon: float = None) -> Dict:
        """Get current weather data for a city or coordinates"""
        params = {
            'appid': self.api_key,
            'units': 'metric'
        }
        
        if city:
            params['q'] = city
        elif lat and lon:
            params['lat'] = lat
            params['lon'] = lon
        else:
            raise ValueError("Either city name or coordinates must be provided")
            
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Add timestamp
            data['timestamp'] = datetime.now().isoformat()
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return {}
    
    def get_forecast(self, city: str = None, lat: float = None, lon: float = None, days: int = 5) -> Dict:
        """Get weather forecast data"""
        params = {
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        if city:
            params['q'] = city
        elif lat and lon:
            params['lat'] = lat
            params['lon'] = lon
        else:
            raise ValueError("Either city name or coordinates must be provided")
            
        try:
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            data['timestamp'] = datetime.now().isoformat()
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast data: {e}")
            return {}
    
    def get_multiple_cities_weather(self) -> List[Dict]:
        """Get weather data for all configured cities"""
        weather_data = []
        
        for city_config in self.config['cities']:
            print(f"Fetching weather for {city_config['name']}...")
            
            data = self.get_current_weather(
                lat=city_config['lat'], 
                lon=city_config['lon']
            )
            
            if data:
                data['city_config'] = city_config
                weather_data.append(data)
                
            time.sleep(1)  # Rate limiting
            
        return weather_data
```
