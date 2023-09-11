from telegram.ext import  CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
import requests


async def get_weather(update: Update, context: CallbackContext):
    try:
        api_key = '29ce7f8a85c561dbfebfab2c44ef5e57'
        url = "https://api.openweathermap.org/data/2.5/weather"
        city_name = "Kyiv"
        params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric"
        }

        response = requests.get(url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            
            await update.callback_query.message.reply_text(
                f"Weather in Kyiv:\n🌡 Temperature: {temperature}°C\n💧 Humidity: {humidity}%\n🌬 Wind speed: {wind_speed} m/s"
                )
        else:
            await update.callback_query.message.reply_text(f"City {city_name} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        