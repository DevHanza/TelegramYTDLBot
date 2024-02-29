import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot
# from telebot import apihelper

import pytube
from y2mate_api import Handler

import os
import re

from dotenv import load_dotenv, dotenv_values 
load_dotenv()
# My custom modules
from modules import downloader

# Enable Logging
# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

# Importing the BOT TOKEN from the .env file.

TOKEN = os.getenv("BOT_API_KEY")

# apihelper.API_URL = "http://0.0.0.0:8081/bot{0}/{1}"

# You can set parse_mode by default. HTML or MARKDOWN
bot = AsyncTeleBot(TOKEN, parse_mode="HTML")
# tb = telebot.AsyncTeleBot("TOKEN")


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(
        message, "Hello, I'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type the /help command.")

@bot.message_handler(commands=['help'])
async def send_help(message):
    await bot.reply_to(
        message, f"<b>How to use?</b> 📝\n\nJust send a youtube video link <b>OR</b> Use @vid to search a video to download.\n\n<i>Share: @YoutubeDownloader4K0_bot.</i>\n<i>Source: https://github.com/hansanaD/TelegramYTDLBot</i>",
        disable_web_page_preview=True
        )

@bot.message_handler(commands=['ping'])
async def send_ping(message):
    await bot.reply_to(
        message, "<b>Pong!</b> 🤖")

@bot.message_handler(commands=['donate'])
async def send_donate(message):
    await bot.reply_to(
        message, "<b>Contact @dev00111_bot for Donations! 🤗</b>")


@bot.message_handler(func=lambda m: True)
async def check_link(message):

    linkFilter = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    userLinks = re.findall(linkFilter, message.text)

    yt_link = []
    for link in userLinks:
        if 'youtube.com' in link or 'youtu.be' in link:
            yt_link.append(link)

    if yt_link:
        # bot.reply_to(message, "YouTube links found.")

        global videoURL
        global api
        global ytThumbMsg
        global yt

        videoURL = yt_link[0]
        api = Handler(videoURL)
        yt = pytube.YouTube(videoURL)

        ytThumbMsg = await bot.send_photo(message.chat.id, yt.thumbnail_url, caption=f"<b>{yt.title}</b>\n\n<b>Link:</b> {videoURL}")
        await showVids(message=message)

    else:
        await bot.reply_to(message, "No YouTube links found!")



async def showVids(message):

    global loadingMsg
    loadingMsg = await bot.reply_to(message, "Looking for Available Qualities..🔎")
    
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
        button = types.InlineKeyboardButton(text=f"{value['q']}  ─  ({value['size']})", callback_data=callbackData)
        markup.add(button) 

    await bot.edit_message_text(chat_id=message.chat.id, message_id=loadingMsg.message_id, text="Choose a stream:", reply_markup=markup)



# Callback handler for # getVidInfo() 
@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):

    receivedData = call.data
    # print(receivedData)

    await bot.answer_callback_query(call.id, f"Selected {receivedData} to download.")

    await downloader.download(bot=bot, yt=yt, message=call.message, userInput=receivedData, videoURL=videoURL, loadingMsg=loadingMsg, ytThumbMsg=ytThumbMsg)



print("TelegramYTDLBot is running..")
import asyncio
asyncio.run(bot.infinity_polling())
