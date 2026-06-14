# Weather Dashboard

**Difficulty**: Intermediate-Advanced  
**Time**: 60-90 minutes  
**Learning Focus**: API integration, data visualisation, environmental data analysis  
**Module**: chat

## Overview

Create a weather dashboard that fetches real-time weather data and forecasts from an API, then visualizes it with charts and provides AI-powered weather advice based on conditions.

## Instructions

```python
import requests
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
from hands_on_ai.chat import get_response

class WeatherDashboard:
    """
    A simple weather dashboard that retrieves and displays weather data.
    Students will need to sign up for a free API key from OpenWeatherMap.
    """
    
    def __init__(self):
        self.api_key = None
        self.base_url = "https://api.openweathermap.org/data/2.5/"
        self.output_dir = "weather_dashboard"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def setup(self):
        """Set up the dashboard with the API key."""
        print("=== Weather Dashboard Setup ===")

        # Read the API key from an environment variable. Never hard-code secrets
        # or write them to a file in your project folder — they can be committed
        # to git by accident. Set it in your shell instead:
        #   export OPENWEATHER_API_KEY="your-key"   (macOS/Linux)
        #   setx OPENWEATHER_API_KEY "your-key"     (Windows)
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")

        # If it isn't set, prompt for one (used only for this session)
        if not self.api_key:
            print("\nYou need an OpenWeatherMap API key to use this dashboard.")
            print("Get a free API key at: https://openweathermap.org/api")
            print("Tip: set OPENWEATHER_API_KEY in your environment to skip this prompt.")
            self.api_key = input("Enter your API key: ").strip()
    
    def get_current_weather(self, location):
        """Get current weather for a location."""
        url = f"{self.base_url}weather"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric'  # Use metric by default
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Location '{location}' not found. Please check the spelling.")
            else:
                print(f"HTTP error: {http_err}")
            return None
        except Exception as err:
            print(f"Error: {err}")
            return None
    
    def get_forecast(self, location, days=5):
        """Get weather forecast for a location."""
        url = f"{self.base_url}forecast"
        params = {
            'q': location,
            'appid': self.api_key,
            'units': 'metric',
            'cnt': days * 8  # API returns data in 3-hour steps, 8 per day
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                print(f"Location '{location}' not found. Please check the spelling.")
            else:
                print(f"HTTP error: {http_err}")
            return None
        except Exception as err:
            print(f"Error: {err}")
            return None
    
    def display_current_weather(self, data):
        """Display current weather conditions."""
        if not data:
            return
        
        try:
            city = data['name']
            country = data['sys']['country']
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            weather_desc = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            clouds = data['clouds']['all']
            
            # Convert Unix timestamp to readable format
            sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
            sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
            
            print("\n=== Current Weather Conditions ===")
            print(f"Location: {city}, {country}")
            print(f"Weather: {weather_desc.title()}")
            print(f"Temperature: {temp}°C (Feels like: {feels_like}°C)")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure} hPa")
            print(f"Wind Speed: {wind_speed} m/s")
            print(f"Cloud Cover: {clouds}%")
            print(f"Sunrise: {sunrise}")
            print(f"Sunset: {sunset}")
            
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
    
    def plot_forecast(self, data, location):
        """Create forecast plots and save them."""
        if not data:
            return
        
        try:
            # Extract forecast data
            timestamps = []
            temps = []
            humidity = []
            descriptions = []
            
            for item in data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                timestamps.append(dt)
                temps.append(item['main']['temp'])
                humidity.append(item['main']['humidity'])
                descriptions.append(item['weather'][0]['description'])
            
            # Create temperature forecast plot
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, temps, marker='o', color='#FF5733', linewidth=2)
            plt.xlabel('Date & Time')
            plt.ylabel('Temperature (°C)')
            plt.title(f'Temperature Forecast for {location}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            temp_plot_file = os.path.join(self.output_dir, f"{location.replace(',', '_')}_temp_forecast.png")
            plt.savefig(temp_plot_file)
            plt.close()
            
            # Create humidity forecast plot
            plt.figure(figsize=(12, 6))
            plt.plot(timestamps, humidity, marker='s', color='#3498DB', linewidth=2)
            plt.xlabel('Date & Time')
            plt.ylabel('Humidity (%)')
            plt.title(f'Humidity Forecast for {location}')
            plt.grid(True, linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save the plot
            humidity_plot_file = os.path.join(self.output_dir, f"{location.replace(',', '_')}_humidity_forecast.png")
            plt.savefig(humidity_plot_file)
            plt.close()
            
            print(f"\nForecast plots saved to:\n- {temp_plot_file}\n- {humidity_plot_file}")
            
            return temp_plot_file, humidity_plot_file
            
        except KeyError as e:
            print(f"Error parsing forecast data: {e}")
            return None, None
    
    def get_weather_summary(self, current_data, forecast_data, location):
        """Generate a summary of the weather conditions and forecast."""
        if not current_data or not forecast_data:
            return "Unable to generate weather summary due to missing data."
        
        try:
            # Extract key information
            current_temp = current_data['main']['temp']
            current_desc = current_data['weather'][0]['description']
            
            # Get min/max for the next few days
            daily_temps = {}
            for item in forecast_data['list']:
                dt = datetime.fromtimestamp(item['dt'])
                date_str = dt.strftime('%Y-%m-%d')
                
                if date_str not in daily_temps:
                    daily_temps[date_str] = {'temps': [], 'descs': []}
                
                daily_temps[date_str]['temps'].append(item['main']['temp'])
                daily_temps[date_str]['descs'].append(item['weather'][0]['description'])
            
            # Create summary with key info
            summary = f"Weather Summary for {location}:\n\n"
            summary += f"Current Conditions: {current_desc.title()} at {current_temp}°C\n\n"
            summary += "Forecast:\n"
            
            for date_str, data in daily_temps.items():
                if data['temps']:  # Make sure we have data
                    min_temp = min(data['temps'])
                    max_temp = max(data['temps'])
                    
                    # Get most common description
                    from collections import Counter
                    desc_counter = Counter(data['descs'])
                    most_common_desc = desc_counter.most_common(1)[0][0]
                    
                    # Format date nicely (e.g., "Monday, Jan 15")
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%A, %b %d')
                    
                    summary += f"- {formatted_date}: {most_common_desc.title()}, {min_temp}°C to {max_temp}°C\n"
            
            return summary
            
        except KeyError as e:
            print(f"Error generating weather summary: {e}")
            return "Unable to generate weather summary."
    
    def get_ai_weather_advice(self, current_data, forecast_data, location):
        """Get AI-generated weather advice based on conditions."""
        if not current_data or not forecast_data:
            return "Unable to generate weather advice due to missing data."
        
        try:
            # Prepare weather information for the AI
            current_temp = current_data['main']['temp']
            current_desc = current_data['weather'][0]['description']
            current_humidity = current_data['main']['humidity']
            current_wind = current_data['wind']['speed']
            
            # Extract forecast information
            tomorrow_data = forecast_data['list'][:8]  # First 8 entries (24 hours)
            tomorrow_descs = [item['weather'][0]['description'] for item in tomorrow_data]
            tomorrow_temps = [item['main']['temp'] for item in tomorrow_data]
            
            avg_tomorrow_temp = sum(tomorrow_temps) / len(tomorrow_temps)
            min_tomorrow_temp = min(tomorrow_temps)
            max_tomorrow_temp = max(tomorrow_temps)
            
            # Create prompt for AI
            prompt = f"""
            Based on the following weather data for {location}:
            
            Current conditions:
            - Temperature: {current_temp}°C
            - Description: {current_desc}
            - Humidity: {current_humidity}%
            - Wind speed: {current_wind} m/s
            
            Tomorrow's forecast:
            - Average temperature: {avg_tomorrow_temp:.1f}°C
            - Range: {min_tomorrow_temp:.1f}°C to {max_tomorrow_temp:.1f}°C
            - Conditions: {', '.join(set(tomorrow_descs))}
            
            Please provide:
            1. Practical advice for what to wear or prepare for today
            2. Any weather warnings or precautions to be aware of
            3. Suggested activities that would be appropriate for this weather
            
            Keep your response conversational and under 150 words.
            """
            
            try:
                advice = get_response(prompt)
                return advice
            except Exception as e:
                print(f"Error getting AI weather advice: {e}")
                return "Unable to generate AI weather advice at this time."
                
        except KeyError as e:
            print(f"Error preparing data for AI advice: {e}")
            return "Unable to generate weather advice due to missing data."
    
    def run(self):
        """Run the main dashboard interface."""
        self.setup()
        
        if not self.api_key:
            print("No API key provided. Exiting.")
            return
        
        print("\n=== Weather Dashboard ===")
        location = input("Enter a city name (e.g., 'London' or 'London,UK'): ")
        
        print(f"\nFetching weather data for {location}...")
        current_data = self.get_current_weather(location)
        
        if current_data:
            self.display_current_weather(current_data)
            
            # Get forecast data
            print("\nFetching forecast data...")
            forecast_data = self.get_forecast(location)
            
            if forecast_data:
                # Plot forecast
                temp_plot, humidity_plot = self.plot_forecast(forecast_data, location)
                
                # Generate weather summary
                summary = self.get_weather_summary(current_data, forecast_data, location)
                print("\n=== Weather Summary ===")
                print(summary)
                
                # Get AI advice if requested
                get_advice = input("\nWould you like personalized weather advice? (y/n): ").lower() == 'y'
                if get_advice:
                    print("\nGenerating advice...")
                    advice = self.get_ai_weather_advice(current_data, forecast_data, location)
                    print("\n=== Weather Advice ===")
                    print(advice)
                
                # Save all info to a report file
                save_report = input("\nSave a weather report file? (y/n): ").lower() == 'y'
                if save_report:
                    try:
                        report_file = os.path.join(self.output_dir, f"{location.replace(',', '_')}_weather_report.txt")
                        with open(report_file, 'w') as f:
                            f.write(f"Weather Report for {location}\n")
                            f.write(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                            f.write("=== Current Conditions ===\n")
                            
                            # Extract current conditions
                            f.write(f"Temperature: {current_data['main']['temp']}°C\n")
                            f.write(f"Feels like: {current_data['main']['feels_like']}°C\n")
                            f.write(f"Weather: {current_data['weather'][0]['description'].title()}\n")
                            f.write(f"Humidity: {current_data['main']['humidity']}%\n")
                            f.write(f"Wind speed: {current_data['wind']['speed']} m/s\n")
                            f.write(f"Pressure: {current_data['main']['pressure']} hPa\n\n")
                            
                            # Add summary
                            f.write("=== Forecast Summary ===\n")
                            f.write(summary + "\n\n")
                            
                            # Add advice if it was generated
                            if get_advice:
                                f.write("=== Weather Advice ===\n")
                                f.write(advice + "\n")
                            
                            # Add note about plot files
                            if temp_plot and humidity_plot:
                                f.write("\nForecast plots saved as:\n")
                                f.write(f"- {os.path.basename(temp_plot)}\n")
                                f.write(f"- {os.path.basename(humidity_plot)}\n")
                        
                        print(f"\nWeather report saved to: {report_file}")
                    except Exception as e:
                        print(f"Error saving weather report: {e}")
            
        print("\nThank you for using the Weather Dashboard!")

# Run the dashboard
if __name__ == "__main__":
    dashboard = WeatherDashboard()
    dashboard.run()
```

## Extension Ideas

- Add support for multiple locations and comparison views
- Implement unit conversion between metric and imperial
- Create a historical weather data retrieval and analysis feature
- Add precipitation and wind forecasts with appropriate visualisations
- Implement a daily weather notification system
- Create a map-based visualisation of weather data

---