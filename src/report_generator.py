```python
import json
import pandas as pd
from datetime import datetime
from typing import Dict, List
import os

class ReportGenerator:
    def __init__(self, output_path: str = "reports/"):
        self.output_path = output_path
        os.makedirs(output_path, exist_ok=True)
    
    def generate_html_report(self, df: pd.DataFrame, metrics: Dict, alerts: List[Dict]) -> str:
        """Generate a comprehensive HTML report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Weather Data Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 20px; text-align: center; }}
                .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #f9f9f9; border-radius: 5px; }}
                .alert {{ background-color: #ffebee; border-left: 5px solid #f44336; padding: 10px; margin: 10px 0; }}
                .data-table {{ width: 100%; border-collapse: collapse; }}
                .data-table th, .data-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                .data-table th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Weather Data Analysis Report</h1>
                <p>Generated on: {timestamp}</p>
            </div>
            
            <div class="section">
                <h2>Summary Statistics</h2>
                <div class="metric">
                    <h3>Average Temperature</h3>
                    <p>{metrics['summary']['avg_temperature']:.1f}°C</p>
                </div>
                <div class="metric">
                    <h3>Temperature Range</h3>
                    <p>{metrics['summary']['min_temperature']:.1f}°C - {metrics['summary']['max_temperature']:.1f}°C</p>
                </div>
                <div class="metric">
                    <h3>Average Humidity</h3>
                    <p>{metrics['summary']['avg_humidity']:.1f}%</p>
                </div>
                <div class="metric">
                    <h3>Average Wind Speed</h3>
                    <p>{metrics['summary']['avg_wind_speed']:.1f} m/s</p>
                </div>
            </div>
            
            <div class="section">
                <h2>Weather Alerts</h2>
        """
        
        if alerts:
            for alert in alerts:
                html_content += f"""
                <div class="alert">
                    <strong>{alert['city']}</strong>: {alert['message']}
                </div>
                """
        else:
            html_content += "<p>No weather alerts at this time.</p>"
        
        html_content += """
            </div>
            
            <div class="section">
                <h2>City Data</h2>
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>City</th>
                            <th>Temperature (°C)</th>
                            <th>Feels Like (°C)</th>
                            <th>Humidity (%)</th>
                            <th>Wind Speed (m/s)</th>
                            <th>Weather</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        for _, row in df.iterrows():
            html_content += f"""
                        <tr>
                            <td>{row['city']}</td>
                            <td>{row['temperature']:.1f}</td>
                            <td>{row['feels_like']:.1f}</td>
                            <td>{row['humidity']}</td>
                            <td>{row['wind_speed']:.1f}</td>
                            <td>{row['weather_description']}</td>
                        </tr>
            """
        
        html_content += """
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>Analysis Insights</h2>
                <h3>Temperature Analysis</h3>
                <ul>
        """
        
        temp_analysis = metrics.get('temperature_analysis', {})
        html_content += f"""
                    <li>Hottest city: {temp_analysis.get('hottest_city', 'N/A')}</li>
                    <li>Coldest city: {temp_analysis.get('coldest_city', 'N/A')}</li>
                    <li>Temperature range: {temp_analysis.get('temperature_range', 0):.1f}°C</li>
                    <li>Cities above average temperature: {temp_analysis.get('cities_above_average', 0)}</li>
                </ul>
                
                <h3>Weather Conditions</h3>
                <ul>
        """
        
        weather_analysis = metrics.get('weather_conditions', {})
        condition_dist = weather_analysis.get('condition_distribution', {})
        for condition, count in condition_dist.items():
            html_content += f"<li>{condition}: {count} cities</li>"
        
        html_content += """
                </ul>
            </div>
        </body>
        </html>
        """
        
        timestamp_file = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_report_{timestamp_file}.html"
        filepath = os.path.join(self.output_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report generated: {filepath}")
        return filepath
    
    def generate_json_report(self, df: pd.DataFrame, metrics: Dict, alerts: List[Dict]) -> str:
        """Generate a JSON report for API consumption"""
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': metrics.get('summary', {}),
            'analysis': {
                'temperature': metrics.get('temperature_analysis', {}),
                'weather_conditions': metrics.get('weather_conditions', {}),
                'wind': metrics.get('wind_analysis', {}),
                'humidity': metrics.get('humidity_analysis', {})
            },
            'alerts': alerts,
            'city_data': df.to_dict('records'),
            'total_cities_analyzed': len(df),
            'report_metadata': {
                'data_source': 'OpenWeatherMap API',
                'analysis_type': 'Real-time Weather Analysis',
                'report_version': '1.0'
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"weather_report_{timestamp}.json"
        filepath = os.path.join(self.output_path, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON report generated: {filepath}")
        return filepath
    
    def generate_summary_text(self, metrics: Dict, alerts: List[Dict]) -> str:
        """Generate a text summary of the weather analysis"""
        summary = f"""
WEATHER DATA ANALYSIS SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

OVERVIEW:
- Total cities analyzed: {metrics['summary']['total_cities']}
- Average temperature: {metrics['summary']['avg_temperature']:.1f}°C
- Temperature range: {metrics['summary']['min_temperature']:.1f}°C to {metrics['summary']['max_temperature']:.1f}°C
- Average humidity: {metrics['summary']['avg_humidity']:.1f}%
- Average wind speed: {metrics['summary']['avg_wind_speed']:.1f} m/s

TEMPERATURE INSIGHTS:
- Hottest city: {metrics['temperature_analysis'].get('hottest_city', 'N/A')}
- Coldest city: {metrics['temperature_analysis'].get('coldest_city', 'N/A')}
- Cities above average temp: {metrics['temperature_analysis'].get('cities_above_average', 0)}
- Temperature standard deviation: {metrics['temperature_analysis'].get('std_deviation', 0):.1f}°C

WEATHER CONDITIONS:
- Most common condition: {metrics['weather_conditions'].get('most_common_condition', 'N/A')}

WIND ANALYSIS:
- Maximum wind speed: {metrics['wind_analysis'].get('max_wind_speed', 0):.1f} m/s
- Windiest city: {metrics['wind_analysis'].get('windiest_city', 'N/A')}
- Cities with high wind: {metrics['wind_analysis'].get('cities_with_high_wind', 0)}

HUMIDITY ANALYSIS:
- Most humid city: {metrics['humidity_analysis'].get('most_humid_city', 'N/A')}
- High humidity cities (>70%): {metrics['humidity_analysis'].get('high_humidity_cities', 0)}
- Low humidity cities (<30%): {metrics['humidity_analysis'].get('low_humidity_cities', 0)}

WEATHER ALERTS:
"""
        
        if alerts:
            for alert in alerts:
                summary += f"- {alert['city']}: {alert['message']}\n"
        else:
            summary += "- No weather alerts detected\n"
        
        summary += f"""
RECOMMENDATIONS:
- Monitor cities with extreme temperatures for potential health impacts
- Consider wind conditions for outdoor activities
- Track humidity levels for comfort assessments
- Review weather patterns for trend analysis

Report generated by Weather Data Analysis System
"""
        
        return summary
