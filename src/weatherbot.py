import telebot
import logging
from telebot import util, types
from telebot import types
from dotenv import load_dotenv
from os import getenv
from time import sleep
from functions import Coordinates
# from functions import Unutilized_Class
# from functions import Misc_Functions

logger = telebot.telebot.logger
logger.setLevel(logging.INFO)

load_dotenv()

# BOT_KEY = getenv('BOT_KEY') # Production bot key
BOT_KEY = getenv('TEST_BOT') # Test bot key
bot = telebot.TeleBot(BOT_KEY, parse_mode=None)
geo_code = Coordinates() # class needs to be initialized here for it's methods to work


"""
Public Group Functions:
- Intentionally limited at this point of development
- For security concerns, the bot will handle location-based requests in private chats
- Still need to re-introduce:
    - Alerts functionality
    - API Status
    - Legal Info
"""

@bot.message_handler(chat_types=['group', 'supergroup', 'channel'], commands=['start'])
def send_welcome(message):
    logger.info(f"""Start command received:\n\n{message.chat.id} - {message.chat.title} - {message.chat.type}\n""")
    bot.reply_to(message, "Keep an eye out for a direct message from me.")
    sleep(2)
    bot.send_message(message.from_user.id, "Hi, I'm WeatherBot!\n\nSend me your location to get the weather in your area.\n\nSend /help for more info on commands.")



"""
Private Chat Functions:
- User must send a location first
- User will be prompted to send it if /start is sent without a location
- Callback handlers for 3 Day and Hourly Forecasts
"""

@bot.message_handler(chat_types=['private'], content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    user_id = message.from_user.id
    logger.info(f"""Location received - Private chat\n\n{message.from_user.id} - {message.location.latitude}, {message.location.longitude}\n""")
    geo_code.update_geocoding(user_id, latitude, longitude)
    bot.reply_to(message, "Location received, send /start to begin.")


@bot.message_handler(chat_types=['private'], commands=['start'])

def start_command(message):
    logger.info(f"""Start command received:\n\n{message.chat.id} - {message.chat.type}\n""")
    user_id = message.from_user.id

    try:
        if geo_code.grids[user_id] != None:
            mkup = types.InlineKeyboardMarkup(row_width=2)
            itembtn1 = types.InlineKeyboardButton("3 Day Forecast", callback_data="3day")
            itembtn2 = types.InlineKeyboardButton("Hourly Forecast", callback_data="hourly")
            mkup.add(itembtn1, itembtn2)
            text = "What would you like to see?"
            bot.send_message(message.chat.id, text, reply_markup=mkup)

    except KeyError:
        logger.info(f"ERROR: No location found for user")
        bot.send_message(user_id, "Error: Please send me your location first, I can't get the weather for your area without it.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id

    if call.data == "3day":
        logger.info(f"3 Day Forecast button pressed\n")
        logger.info(f"{call.from_user.id}")
        bot.answer_callback_query(call.id, text="3 Day Forecast")
        bot.send_message(user_id, geo_code.get_forecast(user_id))

    elif call.data == "hourly":
        logger.info(f"Hourly Forecast button pressed\n")
        bot.answer_callback_query(call.id, text="Hourly Forecast")
        bot.send_message(user_id, geo_code.get_hourly_forecast(user_id))

    else:
        logger.info(f"Unknown button pressed\n")
        bot.answer_callback_query(call.id, text="Error")
        bot.send_message(call.message.chat.id, "Error")


bot.infinity_polling(interval=0, timeout=15)