#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

import os
from dotenv import load_dotenv
import requests as r
import datetime
from telebot import TeleBot

load_dotenv()

API_KEY = os.getenv('API_KEY')
BOT_KEY = os.getenv('BOT_KEY')

# API url
url = f"http://api.openweathermap.org/data/2.5/forecast?"\
        f"id=5128581&units=imperial&cnt=1&appid={API_KEY}"

# make a request to get data
data = r.get(url).json()

# gets us the date (&time if we want it, not neccessary here)
now = datetime.datetime.now().strftime('%A, %B %dth, %Y')


# gets the specific data the bot will send as a string
def parseData():
    header = f"Good morning New York City,\n\nToday is {now}\n\nHere is the forecast for today:\n\n"
    for forecast in data['list'][0:5]:
        output = f"""{header}Weather Conditions: {forecast['weather'][0]['main'].title()}
        Description: {forecast['weather'][0]['description'].title()}
        Temperature: {int(forecast['main']['temp'])}˚ F
        Humidity: {int(forecast['main']['humidity'])}%
        Feels like: {int(forecast['main']['feels_like'])}˚ F
        High: {int(forecast['main']['temp_max'])}˚ F
        Low: {int(forecast['main']['temp_min'])}˚ F
        Wind speed: {int(forecast['wind']['speed'])} mph"""
        return output


app = TeleBot(__name__)

# example /command functionality
# @app.route('/command ?(.*)')
# def core_function(message, cmd):
#     chat_dest = message['chat']['id']
#     msg = "Command Recieved: {}".format(cmd)
#     app.send_message(chat_dest, msg)

# /start function
@app.route('/start ?(.*)')
def start(message, cmd):
    chat_dest = message['chat']['id']
    app.send_message(chat_dest, parseData())

# /help message
@app.route('/help ?(.*)')
def start(message, cmd):
    chat_dest = message['chat']['id']
    msg = "Run /start to get the weather report, or run /help to see this message again."
    app.send_message(chat_dest, msg)

# misc reply for any message received
@app.route('(?!/).+')
def parrot(message):
   chat_dest = message['chat']['id']
   msg = "I only know /start and /help. And yes, those commands are case-sensitive." #.format(user_msg) # this will include their message in the bot's reply
   app.send_message(chat_dest, msg)


if __name__ == '__main__':
    app.config['api_key'] = BOT_KEY
    app.poll(debug=True)