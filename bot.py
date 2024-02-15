import telebot
from telebot import types
import re
import pytube
import os
import sys
from dotenv import dotenv_values

# My custom modules
from modules import vidmerge, progressBar

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

    linkFilter = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    userLinks = re.findall(linkFilter, message.text)

    yt_link = []
    for link in userLinks:
        if 'youtube.com' in link or 'youtu.be' in link:
            yt_link.append(link)

    if yt_link:
        global videoURL
        global yt
        
        videoURL = yt_link[0]
        yt = pytube.YouTube(videoURL, on_progress_callback=progressBar.progress_hook)
        
        bot.reply_to(message, f"Found a YouTube link: {videoURL}", disable_web_page_preview=True)
        getVidInfo(message=message)

    else:
        bot.reply_to(message, "No YouTube links found.")


# Get the available resoultuions of the video
def getVidInfo(message):

    # Thumbnail With Caption
    bot.send_photo(message.chat.id, yt.thumbnail_url, caption=f"Title: {yt.title}\nRating: {yt.rating} \nDuration: {yt.length}")

    bot.reply_to(message, "Looking for Available Qualities..")
    
    streams = yt.streams.filter(only_video=True, mime_type="video/mp4")
    streamsData = []

    for count, stream in enumerate(streams, start=1):
        # print(count, stream.resolution, stream.filesize_mb)
        streamsData.append([count, stream.resolution, stream.filesize_mb])

    print(streamsData)

    # Add Inline Buttons to get user input
    markup = types.InlineKeyboardMarkup() 
    for data in streamsData: 
        callbackData = "#".join(map(str, data))
        button = types.InlineKeyboardButton(text=f"{data[1]} ─ ({data[2]}MB)", callback_data=callbackData)
        markup.add(button) 

    bot.send_message(message.chat.id, "Choose a stream:", reply_markup=markup)

# Callback handler for getVidInfo() 
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # print(call.data)
    received_list = call.data.split("#")
    print(received_list)

    bot.answer_callback_query(call.id, f"Selected {received_list[1]} to download.")

    userInput = int(received_list[0]) - 1
    # downloadVideo(message=call.message, userInput=userInput)


# Download the YouTube Video
def downloadVideo(message, userInput):
    videoID = pytube.extract.video_id(videoURL)
    videoFileName = f"{yt.title}_{videoID}.mp4"
    mediaPath = f"{os.getcwd()}/vids"

    
    streams = yt.streams.filter(only_video=True, mime_type="video/mp4")
    mediaPath = f"{os.getcwd()}/vids"
    
    # print(f"\n\n{type(userInput)}\n\n")
    # print(userInput)

    try:
        # -------VIDEO-------
        bot.send_message(chat_id=message.chat.id, text="<b>Downloading...</b>📥")
        streams[userInput].download(filename=f"{yt.title}.mp4", output_path=mediaPath)
        print("Video Downloaded.")

    except:
        print("Error while downloading the Video.")
        
    try:
        # -------AUDIOS-------
        for stream in yt.streams.filter(only_audio=True, abr="128kbps"):
            stream.download(filename=f"{yt.title}.mp3", output_path=mediaPath)
            print("Audio Downloaded.")    
    except:
        print("Error while downloading the Audio.")

    bot.send_message(chat_id=message.chat.id, text="<b>Processing...♻</b>")

    # Merge the Audio & Video File
    vidmerge.merge(title=f"{yt.title}", outVidTitle=videoFileName)

    bot.send_message(chat_id=message.chat.id, text="<b>Uploading...📤</b>")

    # Upload the video to Telegram
    with open(f"vids/{videoFileName}", 'rb') as file:
        bot.send_document(message.chat.id, file)

    bot.send_message(message.chat.id, "<b>Downloaded...✅</b>")

    # Remove the Media Files
    deleteMedia(mediaPath, videoFileName)


def deleteMedia(mediaPath, videoFileName):
    os.remove(f"{mediaPath}/{yt.title}.mp4")
    os.remove(f"{mediaPath}/{yt.title}.mp3")
    os.remove(f"{mediaPath}/{videoFileName}")
    print("File was sent to User & Deleted from local.")


print("TelegramYTDLBot is running..")
bot.infinity_polling()
