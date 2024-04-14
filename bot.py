import os
import telebot
from telebot import types

from modules import checker, downloader

from dotenv import load_dotenv, dotenv_values 
load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
                      
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, "Hello, I'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type the /help command.")
    

@bot.message_handler(func=lambda m: True)
def link_check(message):
    checker.linkCheck(bot=bot, message=message)
    # print(checker.videoURL)

# Callback handler for # getVidInfo() 
@bot.callback_query_handler(func=lambda call: [call.data == item for item in checker.showList])
def callback_query(call):

    data = call.data.split("#")
    receivedData = data[0]
    videoURL = data[1]
    # print(receivedData)
    
    bot.answer_callback_query(call.id, f"Selected {receivedData} to download.")
    # Delete the message after button got clicked.
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # downloader.download(bot=bot, message=call.message, userInput=receivedData, videoURL=checker.videoURL)
    bot.send_message(call.message.chat.id, f"{videoURL}, {receivedData} : Download Triggered!")
            


print("TelegramYTDLBot is running..")
bot.infinity_polling()
