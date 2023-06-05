from flask import Flask, render_template, request
import requests
import geocoder
from tabulate import tabulate
import dotenv
import os

app = Flask(__name__)


dotenv.load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def get_weather():
    city_name = request.form.get('city_name')

    # Fetch current weather data
    current_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    current_response = requests.get(current_url)

    if current_response.status_code == 200:
        current_data = current_response.json()

        desp = current_data['weather'][0]['description']
        prompt_message = ""

        # Prompt messages based on weather conditions
        if 'rain' in desp.lower():
            prompt_message = "Carry your umbrella, it will rain today."
        elif 'sun' in desp.lower():
            prompt_message = "Wear sunscreen, it's hot today."
        elif 'cloud' in desp.lower():
            if 'scattered' in desp.lower():
                prompt_message = "Expect scattered clouds today."
            elif 'few' in desp.lower():
                prompt_message = "Expect a few clouds today."
            elif 'broken' in desp.lower():
                prompt_message = "Expect broken clouds today."
            elif 'overcast' in desp.lower():
                prompt_message = "Expect overcast clouds today."
            else:
                prompt_message = "It's cloudy today."
        elif 'clear' in desp.lower():
            prompt_message = "It's a clear sky today."
        else:
            prompt_message = "Enjoy the weather!"

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
            return render_template('weather.html', city_name=city_name, current_data=current_data,
                                   forecast_data=table, prompt_message=prompt_message)
        else:
            error_message = f"Error fetching forecast data for {city_name}. Please try again later."
            return render_template('error.html', error_message=error_message)
    else:
        error_message = f"Error fetching current weather data for {city_name}. Please try again later."
        return render_template('error.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
