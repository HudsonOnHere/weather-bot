import telebot
import logging
from telebot import util, types
from telebot import types
from dotenv import load_dotenv
from os import getenv
from time import sleep
from functions import Coordinates, Misc_Functions

logger = telebot.telebot.logger
logger.setLevel(logging.INFO)

load_dotenv()

# BOT_KEY = getenv('BOT_KEY') # Production bot key
BOT_KEY = getenv('TEST_BOT') # Test bot key
bot = telebot.TeleBot(BOT_KEY, parse_mode=None)
geo_code = Coordinates()


@bot.message_handler(chat_types=['group', 'supergroup', 'channel'], commands=['start'])
def send_welcome(message):
    logger.info(f"""Start command received:\n\n{message.chat.id} - {message.chat.title} - {message.chat.type}\n""")
    bot.reply_to(message, "Keep an eye out for a direct message from me.")
    sleep(2)
    bot.send_message(message.from_user.id, "Hi, I'm WeatherBot!\n\nSend me your location to get the weather in your area.\n\nSend /help for more info on commands.")

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
    mkup = types.InlineKeyboardMarkup(row_width=2)
    itembtn1 = types.InlineKeyboardButton("3 Day Forecast", callback_data="3day")
    itembtn2 = types.InlineKeyboardButton("Hourly Forecast", callback_data="hourly")
    mkup.add(itembtn1, itembtn2)
    text = "What would you like to see?"
    bot.send_message(message.chat.id, text, reply_markup=mkup)


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






# @bot.callback_query_handler(func=lambda call: call.data == '3day')
# def a_choosen(call):
#     logger.info(f""""callback_data: 3day, Call ID:{call.id} user ID:{call.from_user.id}\n""")
#     mkup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton("Back", callback_data="back")
#     mkup.add(itembtn1)
#     text = "Updating..."
#     bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup)
#     geo_code.store_call_id(call.from_user.id, call.id)
#     print(geo_code.call_id[call.from_user.id])
#     # global id
#     # id = call.id
    
#     bot.answer_callback_query(callback_query_id=True, show_alert=False)
#     def callback_answer(call):
#         logger.info(f"callback answer triggered")
#         bot.send_message(call.from_user.id, geo_code.get_forecast(Coordinates.get_forecast(call.from_user.id)))

# @bot.answer_callback_query(callback_query_id=id , show_alert=False, cache_time=100)
# def a_choosen(call):
#     # logger.info(f""""callback_data: 3day, Call ID:{call.id}\n""")
#     logger.info(f"answer_callback_query triggered")
#     bot.send_message(call.from_user.id, geo_code.get_forecast(Coordinates.get_forecast(call.from_user.id)))


# @bot.callback_query_handler(func=lambda call: call.data == 'hourly')
# def b_choosen(call):
#     mkup = types.InlineKeyboardMarkup(row_width=1)
#     itembtn1 = types.InlineKeyboardButton("Back", callback_data="back")
#     mkup.add(itembtn1)
#     text = "Hourly Forecast"
#     bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup)
#     bot.send_message(call.message.chat.id, geo_code.get_hourly_forecast(call.message.from_user.id))

# @bot.callback_query_handler(func=lambda call: call.data == 'back')
# def c_choosen(call):
#     mkup = types.InlineKeyboardMarkup(row_width=2)
#     itembtn1 = types.InlineKeyboardButton("3 Day Forecast", callback_data="3day")
#     itembtn2 = types.InlineKeyboardButton("Hourly Forecast", callback_data="hourly")
#     mkup.add(itembtn1, itembtn2)
#     text = "Please choose one."
#     bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=mkup)


bot.infinity_polling(interval=0, timeout=15)