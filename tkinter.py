import requests
import geocoder
from tabulate import tabulate
import tkinter as tk
from tkinter import messagebox

API_KEY = '67616e981465124e28cfcf9cc22d6dc4'
desp="Morning Mist"

def get_current_location():
    g = geocoder.ip('me')
    return g.city

def get_weather(city_name):
    # Fetch current weather data
    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    current_response = requests.get(current_url)

    if current_response.status_code == 200:
        current_data = current_response.json()
        message_text.insert(tk.END, f"\nCurrent weather in {city_name}:\n")
        message_text.insert(tk.END, f"Temperature: {current_data['main']['temp']}°C\n")
        message_text.insert(tk.END, f"Humidity: {current_data['main']['humidity']}%\n")
        message_text.insert(tk.END, f"Wind: {current_data['wind']['speed']} km/h\n")
        message_text.insert(tk.END, f"Description: {current_data['weather'][0]['description']}\n")

        
        desp = current_data['weather'][0]['description']
         # Prompt messages based on weather conditions in the messgae_text widget
        if 'rain' in desp.lower():
            message_text.insert(tk.END, "Carry your umbrella, it will rain today.\n")
        elif 'sun' in desp.lower():
            message_text.insert(tk.END, "Wear sunscreen, it's hot today.\n")
        elif 'cloud' in desp.lower():
            if 'scattered' in desp.lower():
                message_text.insert(tk.END, "Expect scattered clouds today.\n")
            elif 'few' in desp.lower():
                message_text.insert(tk.END, "Expect a few clouds today.\n")
            elif 'broken' in desp.lower():
                message_text.insert(tk.END, "Expect broken clouds today.\n")
            elif 'overcast' in desp.lower():
                message_text.insert(tk.END, "Expect overcast clouds today.\n")
            else:
                message_text.insert(tk.END, "It's cloudy today.\n")
        elif 'clear' in desp.lower():
            message_text.insert(tk.END, "It's a clear sky today.\n")
        else:
            message_text.insert(tk.END, "Enjoy the weather!\n")
    else:
        messagebox.showerror("Error", f"Error fetching current weather data for {city_name}. Please try again later.")
        

    # Fetch forecast data
    forecast_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={API_KEY}&units=metric'
    forecast_response = requests.get(forecast_url)

    if forecast_response.status_code == 200:
        forecast_data = forecast_response.json()

        table_data = []
        headers = ["Date", "Time", "Temperature (°C)", "Humidity", "Wind", "Description"]
        prev_date = None

        for forecast in forecast_data['list']:
            date = forecast['dt_txt'].split()[0]
            time = forecast['dt_txt'].split()[1]
            temperature = forecast['main']['temp']
            humidity = forecast['main']['humidity']
            wind = forecast['wind']['speed']
            description = forecast['weather'][0]['description']

            if prev_date and prev_date != date:
                table_data.append([])  # Add empty row

            table_data.append([date, time, temperature, humidity, wind, description])
            prev_date = date

        table = tabulate(table_data, headers=headers, tablefmt="grid")
        message_text.insert(tk.END, f"\nWeather forecast for the next week in {city_name}:\n")
        message_text.insert(tk.END, table)
    else:
        messagebox.showerror("Error", f"Error fetching forecast data for {city_name}. Please try again later.")

def handle_submit():
    city_name = city_entry.get().strip()
    if city_name:
        message_text.delete(1.0, tk.END)  # Clear previous messages
        get_weather(city_name)
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")

def handle_current_location():
    city_name = get_current_location()
    if city_name:
        message_text.delete(1.0, tk.END)  # Clear previous messages
        get_weather(city_name)
    else:
        messagebox.showwarning("Warning", "Unable to detect current location. Please enter a city name manually.")

# Create GUI window
window = tk.Tk()
window.title("Weather Forecast Tool")
window.geometry("800x600")

# Create label and entry for city name
city_label = tk.Label(window, text="Enter city name:")
city_label.pack()
city_entry = tk.Entry(window)
city_entry.pack()

# Create buttons for submit and current location
submit_button = tk.Button(window, text="Get Weather", command=handle_submit)
submit_button.pack()

current_location_button = tk.Button(window, text="Use Current Location", command=handle_current_location)
current_location_button.pack()

# Create text widget to display messages
#give solution to increase the size of the text box
message_text = tk.Text(window, width=90, height=20)
message_text.pack()


# Start GUI event loop
window.mainloop()
