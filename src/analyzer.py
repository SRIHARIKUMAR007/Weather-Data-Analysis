```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
from datetime import datetime
from typing import Dict, List, Tuple

class WeatherAnalyzer:
    def __init__(self, output_path: str = "reports/"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
        
        # Set style for matplotlib
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def create_temperature_analysis(self, df: pd.DataFrame) -> str:
        """Create temperature analysis visualizations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Temperature distribution
        axes[0, 0].hist(df['temperature'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Temperature Distribution')
        axes[0, 0].set_xlabel('Temperature (°C)')
        axes[0, 0].set_ylabel('Frequency')
        
        # Temperature by city
        df_sorted = df.sort_values('temperature')
        axes[0, 1].barh(df_sorted['city'], df_sorted['temperature'], color='coral')
        axes[0, 1].set_title('Temperature by City')
        axes[0, 1].set_xlabel('Temperature (°C)')
        
        # Temperature vs Humidity scatter
        axes[1, 0].scatter(df['temperature'], df['humidity'], alpha=0.6, s=60)
        axes[1, 0].set_title('Temperature vs Humidity')
        axes[1, 0].set_xlabel('Temperature (°C)')
        axes[1, 0].set_ylabel('Humidity (%)')
        
        # Temperature vs Feels Like
        axes[1, 1].scatter(df['temperature'], df['feels_like'], alpha=0.6, s=60, color='orange')
        axes[1, 1].plot([df['temperature'].min(), df['temperature'].max()], 
                       [df['temperature'].min(), df['temperature'].max()], 
                       'r--', alpha=0.8)
        axes[1, 1].set_title('Temperature vs Feels Like')
        axes[1, 1].set_xlabel('Actual Temperature (°C)')
        axes[1, 1].set_ylabel('Feels Like Temperature (°C)')
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"temperature_analysis_{timestamp}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def create_weather_dashboard(self, df: pd.DataFrame, metrics: Dict) -> str:
        """Create an interactive weather dashboard using Plotly"""
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Temperature by City', 'Weather Conditions Distribution',
                          'Humidity vs Temperature', 'Wind Speed Analysis',
                          'Pressure Distribution', 'Weather Summary'),
            specs=[[{"type": "bar"}, {"type": "pie"}],
                   [{"type": "scatter"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "table"}]]
        )
        
        # Temperature by city
        fig.add_trace(
            go.Bar(x=df['city'], y=df['temperature'], name='Temperature', 
                   marker_color='lightblue'),
            row=1, col=1
        )
        
        # Weather conditions pie chart
        condition_counts = df['weather_main'].value_counts()
        fig.add_trace(
            go.Pie(labels=condition_counts.index, values=condition_counts.values,
                   name="Weather Conditions"),
            row=1, col=2
        )
        
        # Humidity vs Temperature scatter
        fig.add_trace(
            go.Scatter(x=df['temperature'], y=df['humidity'], 
                      mode='markers', name='Humidity vs Temp',
                      text=df['city'], textposition="top center",
                      marker=dict(size=10, opacity=0.7)),
            row=2, col=1
        )
        
        # Wind speed analysis
        fig.add_trace(
            go.Bar(x=df['city'], y=df['wind_speed'], name='Wind Speed',
                   marker_color='lightgreen'),
            row=2, col=2
        )
        
        # Pressure distribution
        fig.add_trace(
            go.Histogram(x=df['pressure'], name='Pressure Distribution',
                        marker_color='lightcoral'),
            row=3, col=1
        )
        
        # Summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Average Temperature', f"{metrics['summary']['avg_temperature']:.1f}°C"],
            ['Max Temperature', f"{metrics['summary']['max_temperature']:.1f}°C"],
            ['Min Temperature', f"{metrics['summary']['min_temperature']:.1f}°C"],
            ['Average Humidity', f"{metrics['summary']['avg_humidity']:.1f}%"],
            ['Average Wind Speed', f"{metrics['summary']['avg_wind_speed']:.1f} m/s"],
        ]
        
        fig.add_trace(
            go.Table(
                header=dict(values=summary_data[0], fill_color='paleturquoise'),
                cells=dict(values=list(zip(*summary_data[1:])), fill_color='lavender')
            ),
            row=3, col=2
        )
        
        fig.update_layout(
            height=1200,
            title_text="Weather Data Dashboard",
            showlegend=False
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_dashboard_{timestamp}.html"
        filepath = os.path.join(self.output_path, filename)
        fig.write_html(filepath)
        
        return filepath
    
    def create_comparative_analysis(self, df: pd.DataFrame) -> str:
        """Create comparative analysis between cities"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Multi-metric comparison
        metrics = ['temperature', 'humidity', 'pressure', 'wind_speed']
        x = np.arange(len(df))
        width = 0.2
        
        for i, metric in enumerate(metrics):
            axes[0, 0].bar(x + i*width, df[metric], width, label=metric, alpha=0.8)
        
        axes[0, 0].set_xlabel('Cities')
        axes[0, 0].set_ylabel('Values (normalized)')
        axes[0, 0].set_title('Multi-Metric Comparison')
        axes[0, 0].set_xticks(x + width * 1.5)
        axes[0, 0].set_xticklabels(df['city'], rotation=45)
        axes[0, 0].legend()
        
        # Correlation heatmap
        correlation_data = df[['temperature', 'humidity', 'pressure', 'wind_speed']].corr()
        im = axes[0, 1].imshow(correlation_data, cmap='coolwarm', aspect='auto')
        axes[0, 1].set_xticks(range(len(correlation_data.columns)))
        axes[0, 1].set_yticks(range(len(correlation_data.columns)))
        axes[0, 1].set_xticklabels(correlation_data.columns, rotation=45)
        axes[0, 1].set_yticklabels(correlation_data.columns)
        axes[0, 1].set_title('Correlation Matrix')
        
        # Add correlation values
        for i in range(len(correlation_data.columns)):
            for j in range(len(correlation_data.columns)):
                axes[0, 1].text(j, i, f'{correlation_data.iloc[i, j]:.2f}',
                               ha="center", va="center", color="black")
        
        # Comfort index (custom metric)
        comfort_index = self.calculate_comfort_index(df)
        axes[1, 0].bar(df['city'], comfort_index, color='lightgreen', alpha=0.7)
        axes[1, 0].set_title('Weather Comfort Index')
        axes[1, 0].set_xlabel('Cities')
        axes[1, 0].set_ylabel('Comfort Index (0-100)')
        axes[1, 0].tick_params(axis='x', rotation=45)
        
        # Weather severity analysis
        severity_scores = self.calculate_weather_severity(df)
        axes[1, 1].bar(df['city'], severity_scores, color='orange', alpha=0.7)
        axes[1, 1].set_title('Weather Severity Score')
        axes[1, 1].set_xlabel('Cities')
        axes[1, 1].set_ylabel('Severity Score')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comparative_analysis_{timestamp}.png"
        filepath = os.path.join(self.output_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filepath
    
    def calculate_comfort_index(self, df: pd.DataFrame) -> List[float]:
        """Calculate a comfort index based on temperature, humidity, and wind"""
        comfort_scores = []
        
        for _, row in df.iterrows():
            temp = row['temperature']
            humidity = row['humidity']
            wind = row['wind_speed']
            
            # Ideal ranges: temp 18-24°C, humidity 40-60%, wind 1-3 m/s
            temp_score = max(0, 100 - abs(temp - 21) * 5)
            humidity_score = max(0, 100 - abs(humidity - 50) * 2)
            wind_score = max(0, 100 - abs(wind - 2) * 20)
            
            comfort_index = (temp_score + humidity_score + wind_score) / 3
            comfort_scores.append(comfort_index)
        
        return comfort_scores
    
    def calculate_weather_severity(self, df: pd.DataFrame) -> List[float]:
        """Calculate weather severity based on extreme conditions"""
        severity_scores = []
        
        for _, row in df.iterrows():
            temp = row['temperature']
            wind = row['wind_speed']
            humidity = row['humidity']
            
            severity = 0
            
            # Temperature extremes
            if temp > 35 or temp < 0:
                severity += abs(temp - 20) * 2
            
            # High wind
            if wind > 10:
                severity += wind * 3
            
            # Extreme humidity
            if humidity > 80 or humidity < 20:
                severity += abs(humidity - 50)
            
            severity_scores.append(min(severity, 100))
        
        return severity_scores
```
