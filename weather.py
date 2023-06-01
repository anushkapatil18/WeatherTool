#API_KEY = '67616e981465124e28cfcf9cc22d6dc4'
import requests
import geocoder
from tabulate import tabulate

API_KEY = '67616e981465124e28cfcf9cc22d6dc4'

#code to get current location
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
        #code for humidity variable
        #humidity unit is in %
        print(f"Humidity: {current_data['main']['humidity']}%")
        #code for wind variable
        #wind unit is in km/h
        print(f"Wind: {current_data['wind']['speed']} km/h")
        print(f"Description: {current_data['weather'][0]['description']}")
        #line space after everyday weather
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


if __name__ == '__main__':
        print("Weather Forecast Tool")
        print("1. Enter a city name")
        print("2. Use current location")

        choice = input("Select an option (1 or 2): ")

        if choice == '1':
            city_name = input("Enter a city name: ")
        elif choice == '2':
            city_name = get_current_location()
            print(f"Detected current location: {city_name}")
        else:
            print("Invalid choice. Exiting...")
            exit()

        get_weather(city_name)







