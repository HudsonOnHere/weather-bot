import logging
import telebot
from telebot import types
from telebot import types
from dotenv import load_dotenv
from os import getenv
from time import sleep
from functions import Location_Functions, Static_Functions

logger = telebot.telebot.logger
logger.setLevel(logging.INFO)

load_dotenv()

BOT_KEY = getenv('TEST_BOT')
MY_ID = getenv('MY_ID') # useful for functions to be utilized by admin only
bot = telebot.TeleBot(BOT_KEY, parse_mode=None)
geo_func = Location_Functions() 
static_func = Static_Functions()


"""
Public Group Functions:
- Intentionally limited at this point of development
- For security concerns, the bot will handle location-based requests in private chats
"""

@bot.message_handler(chat_types=['group', 'supergroup', 'channel'], commands=['start'])
def send_welcome(message):
    logger.info(f"""Start command received: {message.chat.id} - {message.chat.title} - {message.chat.type}""")

    bot.reply_to(message, "Keep an eye out for a direct message from me.")
    sleep(2) # give user a chance to read reply before sending them another, separate msg
    bot.send_message(message.from_user.id, "Hi, I'm WeatherBot!\n\nSend me your location to get the weather in your area.\n\nSend /help for more info on commands.")

@bot.message_handler(chat_types=['group', 'supergroup', 'channel'], commands=['help'])
def send_help(message):
    logger.info(f"Help command received from: {message.from_user.id} - {message.chat.title} - {message.chat.type}")
    
    text = f"""🌦 <b>WeatherBot</b> 🤖 - <i>I can tell you the weather.</i>\n
<u>Send a command to interact with me:</u>\n
🟢 /start - <code>Direct message; location-based weather & alerts</code>\n\n
🟡 /help - <code>I'll display this message</code>\n\n
🔴 /legal - <code>It's 2022, everything needs a disclaimer nowadays</code>"""

    bot.reply_to(message, text, parse_mode='HTML')



"""
Private Chat Functions:
- User must send a location first
- User will be prompted to send it if /start is sent without a location
"""

@bot.message_handler(chat_types=['private'], commands=['help'])
def send_help(message):
    logger.info(f"Help command received from: {message.from_user.id} - {message.chat.title} - {message.chat.type}")
    
    text = f"""🌦 <b>WeatherBot</b> 🤖 - <i>I can tell you the weather.</i>\n
<u>Send a command to interact with me:</u>\n
🟢 /start - <code>First, send your location for weather & alerts</code>\n\n
🟡 /help - <code>I'll display this message</code>\n\n
🔴 /legal - <code>It's 2022, everything needs a disclaimer nowadays</code>"""

    bot.reply_to(message, text, parse_mode='HTML')


@bot.message_handler(chat_types=['private'], content_types=['location'])
def handle_location(message):
    latitude = message.location.latitude
    longitude = message.location.longitude
    user_id = message.from_user.id
    logger.info(f"""Location received - {message.from_user.id} - {message.location.latitude}, {message.location.longitude}""")
    geo_func.update_geocoding(user_id, latitude, longitude)
    bot.reply_to(message, "Location received, send /start to begin.")


@bot.message_handler(chat_types=['private'], commands=['start'])
def start_command(message):
    logger.info(f"""Start command received: {message.chat.id} - {message.chat.type}""")
    user_id = message.from_user.id

    try:
        if geo_func.grids[user_id] != None:
            mkup = types.InlineKeyboardMarkup(row_width=1)
            mkup.add(types.InlineKeyboardButton("3 Day Forecast", callback_data="3day"),
                                            types.InlineKeyboardButton("Hourly Forecast", callback_data="hourly"),
                                            types.InlineKeyboardButton("Alerts", callback_data="alerts"))
            text = "What would you like to see?"
            bot.send_message(message.chat.id, text, reply_markup=mkup)

    except KeyError:
        logger.info(f"ERROR: No location found for user")
        bot.send_message(user_id, "Error: Please send me your location first, I can't get the weather for your area without it.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id
    logger.info(f"""Callback received: {call.from_user.id} - {call.data}""")

    if call.data == "3day":
        logger.info(f"3 Day Forecast button pressed")
        bot.answer_callback_query(call.id, text="3 Day Forecast")
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=geo_func.get_forecast(user_id))

    elif call.data == "hourly":
        logger.info(f"Hourly Forecast button pressed")
        bot.answer_callback_query(call.id, text="Hourly Forecast")
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=geo_func.get_hourly_forecast(user_id))

    elif call.data == "alerts":
        logger.info(f"Alerts button pressed")
        bot.answer_callback_query(call.id, text="Alerts")
        bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id, text=geo_func.get_alerts(user_id))

    else:
        logger.info(f"Unknown button pressed")
        bot.answer_callback_query(call.id, text="Error")
        bot.send_message(call.message.chat.id, "Error")


@bot.message_handler(commands=['status'])
def api_status(message):
    logger.info(f"""Status command received:\n\n{message.from_user.id} - {message.chat.type}""")

    if message.from_user.id == int(MY_ID):
        if static_func.API_status() == True:
            bot.reply_to(message, "API is up and running.")

    else:
        bot.reply_to(message, "Error: Unknown command.")


@bot.message_handler(commands=['legal'])
def legal_info(message):
    logger.info(f"""Legal command received: {message.from_user.id}""")
    bot.reply_to(message, static_func.legal_info())


bot.infinity_polling(interval=0, timeout=15)