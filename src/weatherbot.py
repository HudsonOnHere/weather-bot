import telebot
from dotenv import load_dotenv
import os
from functions import get_forecast, get_hourly_forecast, API_status, get_alerts, legal_info

load_dotenv()

BOT_KEY = os.getenv('BOT_KEY')

bot = telebot.TeleBot(BOT_KEY, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "I'm WeatherBot, I can tell you the weather.\n\nInteract with me by sending one of these commands:\n\n/alerts - gives you the current alerts.\n\n/forecast - gives you the daily forecast.\n\n/hourly - gives you the hourly forecast.\n\n/help - gives you this message.")

@bot.message_handler(commands=['legal'])
def send_license(message):
    bot.reply_to(message, legal_info())

@bot.message_handler(commands=['forecast'])
def send_forecast(message):
    bot.reply_to(message, "Best I can do is like 3 days:\n\n" + get_forecast())

@bot.message_handler(commands=['hourly'])
def send_hourly(message):
    bot.reply_to(message, "Here's what the next 12 hours lookin like:\n\n" + get_hourly_forecast())

@bot.message_handler(commands=['status'])
def send_status(message):
    bot.reply_to(message, API_status())

@bot.message_handler(commands=['alerts'])
def send_alerts(message):
    bot.reply_to(message, get_alerts())

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()