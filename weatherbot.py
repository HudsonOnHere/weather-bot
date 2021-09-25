#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

import os
from dotenv import load_dotenv
import requests as r
import datetime
from telebot import TeleBot

load_dotenv()

class ConnectionError(Exception):
    def __init__(self, error, message="Connection interrupted, reconnecting..."):
        self.error = error
        self.message = message
        super().__init__(self.message)
        


# YOU WILL NEED YOUR OWN API KEYS TO GET THIS WORKING
API_KEY = os.getenv('API_KEY')
BOT_KEY = os.getenv('BOT_KEY')

# weather API url
url = f"http://api.openweathermap.org/data/2.5/forecast?"\
        f"id=5128581&units=imperial&cnt=1&appid={API_KEY}"

# make a request to get data
data = r.get(url).json()

# gets us the date & time
today = datetime.datetime.now().strftime('%A, %B %dth, %Y')
time = datetime.datetime.now().strftime('%H:%M') # will be utilized in next version



# gets the specific data the bot will send as a string
def parseData():
    header = f"Good morning New York City,\n\nToday is {today}\n\nHere is the forecast for today:\n\n"
    for forecast in data['list'][0:5]:
        output = f"""{header}Weather Conditions: {forecast['weather'][0]['main'].title()}
        Description: {forecast['weather'][0]['description'].title()}
        Temperature: {int(forecast['main']['temp'])}˚ F
        Humidity: {int(forecast['main']['humidity'])}%
        Feels like: {int(forecast['main']['feels_like'])}˚ F
        High: {int(forecast['main']['temp_max'])}˚ F
        Low: {int(forecast['main']['temp_min'])}˚ F
        Wind Speed: {int(forecast['wind']['speed'])} mph
        Wind Gusts up to {int(forecast['wind']['gust'])} mph"""
        return output

def weatherBot():
    
    bot = TeleBot(__name__)

    # /weather function
    @bot.route('/weather ?(.*)')
    def weather(message, cmd):
        chat_dest = message['chat']['id']
        bot.send_message(chat_dest, parseData())

    # /help message
    @bot.route('/help ?(.*)')
    def help(message, cmd):
        chat_dest = message['chat']['id']
        msg = "Run /weather to get the weather report, or run /help to see this message again."
        bot.send_message(chat_dest, msg)

    # misc reply for any message received
    @bot.route('(?!/).+')
    def repeat(message):
        chat_dest = message['chat']['id']
        msg = "I only know /weather and /help. And yes, those commands are case-sensitive." #.format(user_msg) # this will include their message in the bot's reply
        bot.send_message(chat_dest, msg)

    if __name__ == '__main__':
        bot.config['api_key'] = BOT_KEY
        bot.poll(debug=True)
        bot.poll(none_stop=True)


while True:
    try:
        weatherBot()
    except:
        raise ConnectionError(weatherBot())
    finally:
        weatherBot()

    