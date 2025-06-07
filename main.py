```python
#!/usr/bin/env python3
"""
Weather Data Analysis System
Main execution script for real-time weather data collection, analysis, and reporting.
"""

import schedule
import time
import sys
import os
from datetime import datetime
from src.weather_api import WeatherAPI
from src.data_processor import WeatherDataProcessor
from src.analyzer import WeatherAnalyzer
from src.report_generator import ReportGenerator

class WeatherAnalysisSystem:
    def __init__(self):
        self.api = WeatherAPI()
        self.processor = WeatherDataProcessor()
        self.analyzer = WeatherAnalyzer()
        self.reporter = ReportGenerator()
        
    def run_analysis(self):
        """Run complete weather analysis workflow"""
        try:
            print(f"\n{'='*50}")
            print(f"Starting Weather Analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*50}")
            
            # Step 1: Collect weather data
            print("1. Collecting weather data...")
            raw_data = self.api.get_multiple_cities_weather()
            
            if not raw_data:
                print("Error: No weather data collected")
                return
            
            print(f"   ✓ Collected data for {len(raw_data)} cities")
            
            # Step 2: Process data
            print("2. Processing weather data...")
            df = self.processor.process_current_weather(raw_data)
            metrics = self.processor.calculate_metrics(df)
            alerts = self.processor.detect_weather_alerts(df)
            
            print(f"   ✓ Processed {len(df)} weather records")
            print(f"   ✓ Generated {len(alerts)} weather alerts")
            
            # Step 3: Save raw and processed data
            print("3. Saving data...")
            self.processor.save_raw_data(raw_data)
            self.processor.save_processed_data(df, metrics, alerts)
            print("   ✓ Data saved successfully")
            
            # Step 4: Generate visualizations
            print("4. Creating visualizations...")
            temp_chart = self.analyzer.create_temperature_analysis(df)
            dashboard = self.analyzer.create_weather_dashboard(df, metrics)
            comparison = self.analyzer.create_comparative_analysis(df)
            
            print(f"   ✓ Temperature analysis: {os.path.basename(temp_chart)}")
            print(f"   ✓ Interactive dashboard: {os.path.basename(dashboard)}")
            print(f"   ✓ Comparative analysis: {os.path.basename(comparison)}")
            
            # Step 5: Generate reports
            print("5. Generating reports...")
            html_report = self.reporter.generate_html_report(df, metrics, alerts)
            json_report = self.reporter.generate_json_report(df, metrics, alerts)
            
            print(f"   ✓ HTML report: {os.path.basename(html_report)}")
            print(f"   ✓ JSON report: {os.path.basename(json_report)}")
            
            # Step 6: Display summary
            print("6. Analysis Summary:")
            summary = self.reporter.generate_summary_text(metrics, alerts)
            print(summary)
            
            print(f"{'='*50}")
            print("Weather analysis completed successfully!")
            print(f"{'='*50}\n")
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            import traceback
            traceback.print_exc()
    
    def start_scheduled_analysis(self, interval_minutes: int = 30):
        """Start scheduled weather analysis"""
        print(f"Starting scheduled weather analysis (every {interval_minutes} minutes)")
        print("Press Ctrl+C to stop")
        
        # Schedule the analysis
        schedule.every(interval_minutes).minutes.do(self.run_analysis)
        
        # Run once immediately
        self.run_analysis()
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nScheduled analysis stopped by user")

def main():
    """Main function with command line interface"""
    system = WeatherAnalysisSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "run":
            # Run analysis once
            system.run_analysis()
            
        elif command == "schedule":
            # Run scheduled analysis
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            system.start_scheduled_analysis(interval)
            
        elif command == "help":
            print("""
Weather Data Analysis System

Usage:
    python main.py run              - Run analysis once
    python main.py schedule [min]   - Run scheduled analysis (default: 30 min)
    python main.py help            - Show this help message

Examples:
    python main.py run
    python main.py schedule 15
    python main.py schedule
            """)
        else:
            print(f"Unknown command: {command}")
            print("Use 'python main.py help' for usage information")
    else:
        # Default: run once
        system.run_analysis()

if __name__ == "__main__":
    main()

