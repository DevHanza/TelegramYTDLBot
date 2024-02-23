import telebot
from telebot import types

import pytube
from y2mate_api import Handler

import os
import re
import sys
from dotenv import dotenv_values

# My custom modules
from modules import downloader

# Enable Logging
# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# Importing the BOT TOKEN from the .env file.
EnvConfig = dotenv_values(".env")
TOKEN = EnvConfig["BOT_API_KEY"]

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, "Hello, I'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type the /help command.")


@bot.message_handler(func=lambda m: True)
def check_link(message):

    linkFilter = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    userLinks = re.findall(linkFilter, message.text)

    yt_link = []
    for link in userLinks:
        if 'youtube.com' in link or 'youtu.be' in link:
            yt_link.append(link)

    if yt_link:
        bot.reply_to(message, "YouTube links found.")

        global videoURL
        global api
        
        videoURL = yt_link[0]
        api = Handler(videoURL)

        showVids(message=message)

    else:
        bot.reply_to(message, "No YouTube links found.")



def showVids(message):
    
    q_list = ['4k', '1080p', '720p', '480p', '360p', '240p']
    # q_list.reverse()

    urlList = []

    def getVidInfo(r):
        for video_metadata in api.run(quality=r):
        
            q = video_metadata.get("q")
            dlink = video_metadata.get("dlink")
            size = video_metadata.get("size")
            
            if dlink == None:
                pass
            else:
                urlList.append([q, size,dlink])
                # print(r, " fetched")
                
    # Iterate over q_list to check if res quality exist on that video
    for r in q_list:
        getVidInfo(r)

    # print(urlList)

    # Create a new list to show
    showList = {}
    for count, item in enumerate(urlList, 1):
        del item[2] # Remove dlink from list
        q = item[0]
        # print(i)
        size = item[1] 
        showList.update( { count: { "q":q, "size": size }} )
    
    # print(showList)

    # Add Inline Buttons to get user input
    markup = types.InlineKeyboardMarkup() 
    for value in showList.values(): 
        callbackData = value["q"]
        button = types.InlineKeyboardButton(text=f"{value["q"]}  ─  ({value["size"]})", callback_data=callbackData)
        markup.add(button) 

    global qualityBtnList
    qualityBtnList = bot.send_message(message.chat.id, "Choose a stream:", reply_markup=markup)


# Callback handler for # getVidInfo() 
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):

    receivedData = call.data
    # print(receivedData)

    bot.answer_callback_query(call.id, f"Selected {receivedData} to download.")

    downloader.download(bot=bot, message=call.message, userInput=receivedData, videoURL=videoURL)



print("TelegramYTDLBot is running..")
bot.infinity_polling()
