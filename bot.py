import telebot
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
        videoURL = yt_link[0]
        foundLinkMsg = bot.reply_to(message, f"Found a YouTube link: {videoURL}", disable_web_page_preview=True)
        downloadVideo(message=message, videoURL=videoURL, foundLinkMsg=foundLinkMsg)

    else:
        bot.reply_to(message, "No YouTube links found.")



def downloadVideo(message, videoURL, foundLinkMsg):

    # Download the video from YouTube using pytube

    # bot.send_photo(message.chat.id, yt.thumbnail_url, caption="yt.title")

    yt = pytube.YouTube(videoURL, on_progress_callback=progressBar.progress_hook)

    # Thumbnail With Caption
    bot.send_photo(message.chat.id, yt.thumbnail_url, caption=f"Title: {yt.title}")

    loading_message = bot.reply_to(message, "Looking for Available Qualities..")

    streams = yt.streams.filter(only_video=True, mime_type="video/mp4")
    mediaPath = f"{os.getcwd()}/vids"

    # -------VIDEOS-------
    streamsData = []

    for count, stream in enumerate(streams, start=1):
        # print(count, stream.resolution, stream.filesize_mb)
        streamsData.append([count, stream.resolution, stream.filesize_mb])

    print(streamsData)

    bot.delete_message(chat_id=message.chat.id, message_id=foundLinkMsg.message_id)
    
    try:
        userInput = 3

        bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text="<b>Downloading...</b>📥")

        streams[userInput].download(filename=f"{yt.title}.mp4", output_path=mediaPath)
        print("Video Downloaded. ✔")

    except:
        print("Wrong Input! Try Again!")
        
    # -------AUDIOS-------

    for stream in yt.streams.filter(only_audio=True, abr="128kbps"):
        stream.download(filename=f"{yt.title}.mp3", output_path=mediaPath)
        print("Audio Downloaded. ✔")

    videoID = pytube.extract.video_id(videoURL)
    videoFileName = f"{yt.title}_{videoID}.mp4"

    bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text="Processing...♻")

    # Merge the Audio & Video File
    vidmerge.merge(title=f"{yt.title}", outVidTitle=videoFileName)

    bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text="Uploading...📤")

    # Upload the video to Telegram
    with open(f"vids/{videoFileName}", 'rb') as file:
        bot.send_document(message.chat.id, file)

    bot.delete_message(chat_id=message.chat.id, message_id=loading_message.message_id)
    bot.reply_to(message, "Downloaded...✅")

    # Remove the Media Files
    os.remove(f"{mediaPath}/{yt.title}.mp4")
    os.remove(f"{mediaPath}/{yt.title}.mp3")
    os.remove(f"{mediaPath}/{videoFileName}")
    print("File was sent to User & Deleted from local.")


print("TelegramYTDLBot is running..")
bot.infinity_polling()
