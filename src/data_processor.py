```python
import pandas as pd
import numpy as np
import json
from datetime import datetime
from typing import Dict, List
import os

class WeatherDataProcessor:
    def __init__(self, data_path: str = "data/"):
        self.data_path = data_path
        self.raw_path = os.path.join(data_path, "raw")
        self.processed_path = os.path.join(data_path, "processed")
        
        # Create directories if they don't exist
        os.makedirs(self.raw_path, exist_ok=True)
        os.makedirs(self.processed_path, exist_ok=True)
    
    def save_raw_data(self, data: List[Dict], filename: str = None) -> str:
        """Save raw weather data to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weather_data_{timestamp}.json"
        
        filepath = os.path.join(self.raw_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Raw data saved to: {filepath}")
        return filepath
    
    def process_current_weather(self, raw_data: List[Dict]) -> pd.DataFrame:
        """Process current weather data into a structured DataFrame"""
        processed_data = []
        
        for data in raw_data:
            try:
                record = {
                    'timestamp': data.get('timestamp'),
                    'city': data.get('name', 'Unknown'),
                    'country': data.get('sys', {}).get('country', 'Unknown'),
                    'latitude': data.get('coord', {}).get('lat'),
                    'longitude': data.get('coord', {}).get('lon'),
                    'temperature': data.get('main', {}).get('temp'),
                    'feels_like': data.get('main', {}).get('feels_like'),
                    'humidity': data.get('main', {}).get('humidity'),
                    'pressure': data.get('main', {}).get('pressure'),
                    'visibility': data.get('visibility'),
                    'wind_speed': data.get('wind', {}).get('speed'),
                    'wind_direction': data.get('wind', {}).get('deg'),
                    'cloudiness': data.get('clouds', {}).get('all'),
                    'weather_main': data.get('weather', [{}])[0].get('main'),
                    'weather_description': data.get('weather', [{}])[0].get('description'),
                    'sunrise': data.get('sys', {}).get('sunrise'),
                    'sunset': data.get('sys', {}).get('sunset'),
                }
                processed_data.append(record)
                
            except Exception as e:
                print(f"Error processing weather data: {e}")
                continue
        
        df = pd.DataFrame(processed_data)
        
        # Convert timestamp to datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Convert sunrise/sunset to datetime
        if 'sunrise' in df.columns:
            df['sunrise'] = pd.to_datetime(df['sunrise'], unit='s')
        if 'sunset' in df.columns:
            df['sunset'] = pd.to_datetime(df['sunset'], unit='s')
            
        return df
    
    def calculate_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate various weather metrics and statistics"""
        if df.empty:
            return {}
        
        metrics = {
            'summary': {
                'total_cities': len(df),
                'avg_temperature': df['temperature'].mean(),
                'max_temperature': df['temperature'].max(),
                'min_temperature': df['temperature'].min(),
                'avg_humidity': df['humidity'].mean(),
                'avg_pressure': df['pressure'].mean(),
                'avg_wind_speed': df['wind_speed'].mean(),
            },
            'temperature_analysis': {
                'std_deviation': df['temperature'].std(),
                'temperature_range': df['temperature'].max() - df['temperature'].min(),
                'cities_above_average': len(df[df['temperature'] > df['temperature'].mean()]),
                'hottest_city': df.loc[df['temperature'].idxmax(), 'city'] if not df.empty else None,
                'coldest_city': df.loc[df['temperature'].idxmin(), 'city'] if not df.empty else None,
            },
            'weather_conditions': {
                'condition_distribution': df['weather_main'].value_counts().to_dict(),
                'most_common_condition': df['weather_main'].mode().iloc[0] if not df['weather_main'].empty else None,
            },
            'wind_analysis': {
                'max_wind_speed': df['wind_speed'].max(),
                'cities_with_high_wind': len(df[df['wind_speed'] > df['wind_speed'].quantile(0.75)]),
                'windiest_city': df.loc[df['wind_speed'].idxmax(), 'city'] if not df.empty else None,
            },
            'humidity_analysis': {
                'high_humidity_cities': len(df[df['humidity'] > 70]),
                'low_humidity_cities': len(df[df['humidity'] < 30]),
                'most_humid_city': df.loc[df['humidity'].idxmax(), 'city'] if not df.empty else None,
            }
        }
        
        return metrics
    
    def detect_weather_alerts(self, df: pd.DataFrame) -> List[Dict]:
        """Detect potential weather alerts based on thresholds"""
        alerts = []
        
        for _, row in df.iterrows():
            city = row['city']
            
            # Temperature alerts
            if row['temperature'] > 40:
                alerts.append({
                    'city': city,
                    'type': 'EXTREME_HEAT',
                    'value': row['temperature'],
                    'message': f"Extreme heat warning: {row['temperature']:.1f}°C"
                })
            elif row['temperature'] < -20:
                alerts.append({
                    'city': city,
                    'type': 'EXTREME_COLD',
                    'value': row['temperature'],
                    'message': f"Extreme cold warning: {row['temperature']:.1f}°C"
                })
            
            # Wind alerts
            if row['wind_speed'] > 20:
                alerts.append({
                    'city': city,
                    'type': 'HIGH_WIND',
                    'value': row['wind_speed'],
                    'message': f"High wind warning: {row['wind_speed']:.1f} m/s"
                })
            
            # Humidity alerts
            if row['humidity'] > 90:
                alerts.append({
                    'city': city,
                    'type': 'HIGH_HUMIDITY',
                    'value': row['humidity'],
                    'message': f"High humidity: {row['humidity']}%"
                })
        
        return alerts
    
    def save_processed_data(self, df: pd.DataFrame, metrics: Dict, alerts: List[Dict]) -> str:
        """Save processed data to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save DataFrame to CSV
        csv_path = os.path.join(self.processed_path, f"processed_weather_{timestamp}.csv")
        df.to_csv(csv_path, index=False)
        
        # Save metrics and alerts to JSON
        json_path = os.path.join(self.processed_path, f"analysis_{timestamp}.json")
        analysis_data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'alerts': alerts
        }
        
        with open(json_path, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        print(f"Processed data saved to: {csv_path}")
        print(f"Analysis saved to: {json_path}")
        
        return csv_path, json_path
```
