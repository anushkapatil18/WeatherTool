import requests
import json
import sys

#login OpenWeatherMap to get API key
#https://home.openweathermap.org/api_keys
#API_KEY = '67616e981465124e28cfcf9cc22d6dc4'
#make a fucntion to get weather data
#time format function
#main function
#check if the user has provided a city name
#call the get_weather function
#python weather.py london
#python weather.py london,uk
#python weather.py "new york"
#python weather.py "new york,us"
#python weather.py "new york" us


API_KEY = '67616e981465124e28cfcf9cc22d6dc4'

def get_weather(city_name):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        sunrise = data['sys']['sunrise']
        sunset = data['sys']['sunset']
        visibility = data['visibility'] / 1000  # Convert visibility from meters to kilometers

        print(f"Current weather in {city_name}:")
        print(f"Temperature: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} m/s")
        print(f"Description: {description}")
        print(f"Sunrise: {format_time(sunrise)}")
        print(f"Sunset: {format_time(sunset)}")
        print(f"Visibility: {visibility} km")
    else:
        print(f"Error fetching weather data for {city_name}. Please try again later.")

def format_time(timestamp):
    import datetime
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide a city name as a command-line argument.")
    else:
        city_name = ' '.join(sys.argv[1:])
        get_weather(city_name)
