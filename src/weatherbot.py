import telebot
from telebot import types, util
from dotenv import load_dotenv
import os
# from functions import FORECAST_GRID, GRID_X, GRID_Y, get_forecast, get_hourly_forecast, get_alerts, API_status, geocoding, legal_info
from functions import *
import logging



logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

load_dotenv()

# BOT_KEY = os.getenv('BOT_KEY')
BOT_KEY = os.getenv('TEST_BOT')

bot = telebot.TeleBot(BOT_KEY, parse_mode=None)

# testing global variables
LATITUDE = 0
LONGITUDE = 0

@bot.message_handler(chat_types=['group', 'supergroup', 'channel'], commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "I just sent you a direct message.")
    bot.send_message(message.from_user.id, "Hi, I'm WeatherBot!\n\nSend me your location to get the weather in your area, or send me /start again for more options.\n\nSend /help for more info on commands.")

# @bot.message_handler(commands=['help'])
# def send_help(message):
#     bot.reply_to(message, "I'm WeatherBot, I can tell you the weather.\n\nInteract with me by sending one of these commands:\n\n/alerts - gives you the current alerts.\n\n/forecast - gives you the daily forecast.\n\n/hourly - gives you the hourly forecast.\n\n/help - gives you this message.")

# @bot.message_handler(commands=['legal'])
# def send_license(message):
#     bot.reply_to(message, legal_info())

# @bot.message_handler(commands=['forecast'])
# def send_forecast(message):
#     bot.reply_to(message, "Best I can do is like 3 days:\n\n" + get_forecast())

# @bot.message_handler(commands=['hourly'])
# def send_hourly(message):
#     bot.reply_to(message, "Here's what the next 12 hours looks like:\n\n" + get_hourly_forecast())

# @bot.message_handler(commands=['status'])
# def send_status(message):
#     bot.reply_to(message, API_status())

# @bot.message_handler(commands=['alerts'])
# def send_alerts(message):
#     bot.reply_to(message, get_alerts())



@bot.message_handler(chat_types=['private'], content_types=['location'])
def handle_location(message):

    global LATITUDE
    global LONGITUDE

    LATITUDE = message.location.latitude
    LONGITUDE = message.location.longitude
    geocoding(LATITUDE, LONGITUDE)

    bot.reply_to(message, f"""This you?? {LATITUDE}, {LONGITUDE}""")
    return LATITUDE, LONGITUDE


@bot.message_handler(chat_types=['private'], commands=['start'])
def starting_point(message):

    if LATITUDE == 0 or LONGITUDE == 0:
        bot.reply_to(message, "Please send me your location first.")
    
    else:
        mkup = types.InlineKeyboardMarkup(row_width=2)
        itembtn1 = types.InlineKeyboardButton("3 Day Forecast", callback_data="3day")
        itembtn2 = types.InlineKeyboardButton("Hourly Forecast", callback_data="hourly")
        mkup.add(itembtn1, itembtn2)
        text = "What would you like to see?"
        bot.send_message(message.chat.id, text, reply_markup=mkup)


@bot.callback_query_handler(func=lambda call: call.data == '3day')
def a_choosen(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    # itembtn1 = types.InlineKeyboardButton("Back", callback_data="back")
    # mkup.add(itembtn1)
    text = "3 Day Forecast"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup)
    bot.send_message(call.message.chat.id, get_forecast(FORECAST_GRID, GRID_X, GRID_Y))


@bot.callback_query_handler(func=lambda call: call.data == 'hourly')
def b_choosen(call):
    mkup = types.InlineKeyboardMarkup(row_width=1)
    # itembtn1 = types.InlineKeyboardButton("Back", callback_data="back")
    # mkup.add(itembtn1)
    text = "Hourly Forecast"
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup)

@bot.callback_query_handler(func=lambda call: call.data == 'back')
def c_choosen(call):
    mkup = types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton("3 Day Forecast", callback_data="3day")
    itembtn2 = types.InlineKeyboardButton("Hourly Forecast", callback_data="hourly")
    mkup.add(itembtn1, itembtn2)
    text = "Hello again! Choose one."
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup)


@bot.message_handler(commands=['test'])
def test_command(message):
    bot.reply_to(message, "Check the console for output, the default values are 0.")
    print(f"Sender: {message.from_user.username}")
    print(f"Latitude: {LATITUDE}")
    print(f"Longitude: {LONGITUDE}")



bot.infinity_polling(interval=0, timeout=15)