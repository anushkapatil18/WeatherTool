import os
import geocoder
from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
import dotenv

dotenv.load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

# Code to get current location
def get_current_location():
    g = geocoder.ip('me')
    return g.city

def get_weather(city_name):
    # Current weather API URL
    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'

     # Forecast API URL for next week
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'

    # Fetch current weather data
    current_response = requests.get(current_url)

    if current_response.status_code == 200:
        current_data = current_response.json()
        print("\n")
        print(f"Current weather in {city_name}:")
        print(f"Temperature: {current_data['main']['temp']}°C")
        # Code for humidity variable
        # Humidity unit is in %
        print(f"Humidity: {current_data['main']['humidity']}%")
        # Code for wind variable
        # Wind unit is in km/h
        print(f"Wind: {current_data['wind']['speed']} km/h")
        print(f"Description: {current_data['weather'][0]['description']}")
        message = prompt_message_based_on_weather(current_data['weather'][0]['description'])
        print(message)
        # Line space after everyday weather
        print("\n")

    else:
        print(f"Error fetching current weather data for {city_name}. Please try again later.")

     # Fetch forecast data
    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()
    
        table_data = []
        headers = ["Date", "Time", "Temperature (°C)","Humidity","Wind", "Description"]
        prev_date = None
        for forecast in forecast_data['list']:
            date = forecast['dt_txt'].split()[0]
            time = forecast['dt_txt'].split()[1]
            temperature = forecast['main']['temp']
            #code for humidity variable
            humidity = forecast['main']['humidity']
            #code for wind variable
            wind = forecast['wind']['speed']
            description = forecast['weather'][0]['description']
            if prev_date and prev_date != date:
                table_data.append([])  # Add empty row

            table_data.append([date, time, temperature,humidity,wind, description])
            prev_date = date
            table_data.append([date, time, temperature,humidity,wind, description])

        print(f"Weather forecast for the next week in {city_name}:\n")
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print(f"Error fetching forecast data for {city_name}. Please try again later.")

def prompt_message_based_on_weather(description):
    description = description.lower()

    if 'rain' in description:
        return "Carry your umbrella, it will rain today."
    elif 'sun' in description or 'clear' in description:
        return "Wear sunscreen, it's sunny today."
    elif 'cloud' in description:
        if 'scattered' in description:
            return "Expect scattered clouds."
        elif 'few' in description:
            return "Expect a few clouds."
        elif 'broken' in description:
            return "Expect broken clouds."
        elif 'overcast' in description:
            return "Expect overcast clouds."
        else:
            return "It's cloudy today."
    elif 'snow' in description:
        return "Bundle up, it's snowing today."
    elif 'wind' in description:
        return "Hold onto your hat, it's windy today."
    elif 'thunderstorm' in description:
        return "Stay indoors, there's a thunderstorm."
    elif 'fog' in description:
        return "Drive carefully, there's fog."
    elif 'haze' in description or 'smoke' in description:
        return "Air quality may be poor, be cautious."
    else:
        return "Enjoy the weather!"

def visualize_weather_comparison(city_names, temperature_data):
    if len(city_names) < 1:
        print("No cities entered. Please enter at least one city.")
        return

    if len(city_names) != len(temperature_data):
        print("Insufficient data to visualize weather comparison. Please make sure data is available for all cities.")
        return

    # Setting the seaborn style
    sns.set(style='darkgrid')

    # Creating a color palette for the bars
    colors = sns.color_palette('Set3', len(city_names))

    # Plotting the temperature data
    x_labels = np.arange(len(city_names))
    plt.figure(figsize=(10, 6))
    plt.bar(x_labels, temperature_data, color=colors)

    # Adding labels and title
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Temperature (°C)', fontsize=12)
    plt.title('Weather Comparison', fontsize=14, fontweight='bold')

    # Customizing tick labels and rotation
    plt.xticks(x_labels, city_names, rotation=45, fontsize=10)

    # Adding a legend
    legend_labels = [f'{city}: {temp}°C' for city, temp in zip(city_names, temperature_data)]
    plt.legend(legend_labels, loc='upper right', fontsize=8)

    # Adding a grid for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Save the figure as an image file
    plt.savefig('weather_comparison.png')

    #print a success message to the user after the image is saved
    print("Weather comparison image saved successfully!")



# Code to get weekly temperature
def get_weekly_temperature(city_name):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    # Check if the response is successful
    # If successful, get the temperature dats
    if response.status_code == 200:
        data = response.json()
        temperatures = [forecast['main']['temp'] for forecast in data['list']]
        avg_temperature = sum(temperatures) / len(temperatures)
        return avg_temperature
    # If unsuccessful, print an error message
    else:
        print(f"Error fetching forecast data for {city_name}. Please try again later.")
        return None
    
if __name__ == '__main__':
    print("Weather Forecast Tool")
    print("1. Enter a city name")
    print("2. Use current location")
    print("3. Compare multiple cities")

    choice = input("Select an option (1, 2, or 3): ")

    if choice == '1':
        city_name = input("Enter a city name: ")
        get_weather(city_name)
    elif choice == '2':
        city_name = get_current_location()
        print(f"Detected current location: {city_name}")
        get_weather(city_name)
    elif choice == '3':
        num_cities = int(input("Enter the number of cities to compare: "))
        city_names = []
        temperature_data = []
        for i in range(num_cities):
            city = input(f"Enter city {i+1} name: ")
            # Add city to list of cities
            city_names.append(city)
            # Get weekly temperature for city
            temperature = get_weekly_temperature(city)
            temperature_data.append(temperature)
            
        visualize_weather_comparison(city_names, temperature_data)
    else:
        print("Invalid choice. Exiting...")
        exit()
