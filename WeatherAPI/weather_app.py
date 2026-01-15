# weather_app.py
import requests
import json
from datetime import datetime

# ===========================================
# CONFIGURATION
# ===========================================
API_KEY = "2b6e29cb829f1dafdac1f316dba32d1d"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# ===========================================
# HELPER FUNCTIONS
# ===========================================
def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

def kelvin_to_fahrenheit(kelvin):
    """Convert Kelvin to Fahrenheit"""
    return (kelvin - 273.15) * 9/5 + 32

def get_wind_direction(degrees):
    """Convert wind degrees to compass direction"""
    directions = ["North", "North-East", "East", "South-East", 
                  "South", "South-West", "West", "North-West"]
    index = round(degrees / 45) % 8
    return directions[index]

def format_time(timestamp, timezone_offset=0):
    """Convert Unix timestamp to readable time"""
    return datetime.fromtimestamp(timestamp + timezone_offset).strftime('%H:%M')

# ===========================================
# MAIN FUNCTION TO FETCH WEATHER
# ===========================================
def get_weather_data(city_name):
    """
    Fetch weather data for a given city
    
    Args:
        city_name (str): Name of the city
    
    Returns:
        dict: Weather data or None if error
    """
    # Prepare API request parameters
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # You can also use 'imperial' for Fahrenheit
    }
    
    try:
        # Make the API request
        print(f"Fetching weather data for {city_name}...")
        response = requests.get(BASE_URL, params=params, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}")
            print(f"Message: {response.json().get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the internet.")
        return None
    except requests.exceptions.Timeout:
        print("Error: Request timed out.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

# ===========================================
# FUNCTION TO DISPLAY WEATHER DATA
# ===========================================
def display_weather_data(weather_data, use_fahrenheit=False):
    """
    Display weather data in a user-friendly format
    
    Args:
        weather_data (dict): Weather data from API
        use_fahrenheit (bool): Whether to display in Fahrenheit
    """
    if not weather_data:
        print("No weather data to display.")
        return
    
    print("\n" + "="*50)
    print("WEATHER INFORMATION")
    print("="*50)
    
    # City and Country
    city = weather_data['name']
    print(f"📊 Timezone: GMT{weather_data['timezone']//3600:+d}")
    
    # Weather Description
    weather_desc = weather_data['weather'][0]['description'].title()
    weather_main = weather_data['weather'][0]['main']
    print(f"🌤️  Weather: {weather_main} ({weather_desc})")
    
    # Temperature
    temp = weather_data['main']['temp']
    temp_min = weather_data['main']['temp_min']
    temp_max = weather_data['main']['temp_max']
    feels_like = weather_data['main']['feels_like']
    
    if use_fahrenheit:
        temp = (temp * 9/5) + 32
        temp_min = (temp_min * 9/5) + 32
        temp_max = (temp_max * 9/5) + 32
        feels_like = (feels_like * 9/5) + 32
        unit = "°F"
    else:
        unit = "°C"
    
    print(f"🌡️  Temperature: {temp:.1f}{unit}")
    print(f"   Feels like: {feels_like:.1f}{unit}")
    print(f"   Min/Max: {temp_min:.1f}{unit} / {temp_max:.1f}{unit}")
    
    # Humidity and Pressure
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    print(f"💧 Humidity: {humidity}%")
    print(f"📊 Pressure: {pressure} hPa")
    
    # Wind
    wind_speed = weather_data['wind']['speed']
    wind_deg = weather_data['wind'].get('deg', 0)
    wind_direction = get_wind_direction(wind_deg)
    
    if use_fahrenheit:
        wind_speed_mph = wind_speed * 2.237
        print(f"💨 Wind: {wind_speed_mph:.1f} mph, {wind_direction}")
    else:
        wind_speed_kmh = wind_speed * 3.6
        print(f"💨 Wind: {wind_speed_kmh:.1f} km/h, {wind_direction}")
    
    # Visibility
    visibility = weather_data.get('visibility', 'N/A')
    if visibility != 'N/A':
        visibility_km = visibility / 1000
        print(f"👁️  Visibility: {visibility_km:.1f} km")
    else:
        print(f"👁️  Visibility: {visibility}")
    
    # Sunrise and Sunset
    sunrise = format_time(weather_data['sys']['sunrise'], weather_data['timezone'])
    sunset = format_time(weather_data['sys']['sunset'], weather_data['timezone'])
    print(f"🌅 Sunrise: {sunrise}")
    print(f"🌇 Sunset: {sunset}")
    
    # Cloudiness
    clouds = weather_data['clouds']['all']
    print(f"☁️  Cloudiness: {clouds}%")
    
    # Coordinates
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    print(f"📍 Coordinates: {lat:.4f}, {lon:.4f}")
    
    print("="*50)

# ===========================================
# FUNCTION TO SAVE WEATHER DATA
# ===========================================
def save_weather_data(weather_data, filename="weather_history.json"):
    """
    Save weather data to a JSON file
    
    Args:
        weather_data (dict): Weather data to save
        filename (str): Name of the file to save to
    """
    try:
        # Try to load existing data
        try:
            with open(filename, 'r') as file:
                history = json.load(file)
        except FileNotFoundError:
            history = []
        
        # Add timestamp to data
        weather_data_with_time = {
            'timestamp': datetime.now().isoformat(),
            'data': weather_data
        }
        
        # Add new data and save (keep last 10 entries)
        history.append(weather_data_with_time)
        if len(history) > 10:
            history = history[-10:]
        
        with open(filename, 'w') as file:
            json.dump(history, file, indent=2)
            
        print(f"✅ Weather data saved to {filename}")
        
    except Exception as e:
        print(f"⚠️  Could not save data: {str(e)}")

# ===========================================
# MAIN PROGRAM EXECUTION
# ===========================================
def main():
    """Main function to run the weather app"""
    
    print("🌤️  WEATHER APPLICATION 🌤️")
    print("-" * 30)
    
    while True:
        # Get city name from user
        city = input("\nEnter city name (or 'quit' to exit): ").strip()
        
        if city.lower() == 'quit':
            print("Goodbye! 👋")
            break
        
        if not city:
            print("Please enter a valid city name.")
            continue
        
        # Get temperature unit preference
        unit_choice = input("Temperature in (C)elsius or (F)ahrenheit? [C/F]: ").strip().upper()
        use_fahrenheit = unit_choice == 'F'
        
        # Fetch weather data
        weather_data = get_weather_data(city)
        
        if weather_data:
            # Display weather data
            display_weather_data(weather_data, use_fahrenheit)
            
            # Ask if user wants to save the data
            save_choice = input("\nSave this weather data? (y/n): ").strip().lower()
            if save_choice == 'y':
                save_weather_data(weather_data)
        
        # Ask if user wants to check another city
        another = input("\nCheck another city? (y/n): ").strip().lower()
        if another != 'y':
            print("Thank you for using the Weather App! 👋")
            break

# ===========================================
# ENTRY POINT
# ===========================================
if __name__ == "__main__":
    # First, check if API key is set
    if API_KEY == "YOUR_API_KEY_HERE":
        print("⚠️  WARNING: You need to add your API key!")
        print("1. Go to https://openweathermap.org/api")
        print("2. Sign up for a free account")
        print("3. Get your API key from the dashboard")
        print("4. Replace 'YOUR_API_KEY_HERE' with your actual key")
        print("\nAfter getting your API key, run the program again.")
    else:
        main()