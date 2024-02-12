import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Custom Imports
from telegram import MessageEntity
from telegram.ext import filters, MessageHandler
from telegram.constants import ParseMode

import pytube
import os ,sys
from dotenv import dotenv_values

# My custom modules
from modules import vidmerge, progressBar

# Importing the BOT TOKEN from the .env file.
EnvConfig = dotenv_values(".env")
TOKEN = EnvConfig["BOT_API_KEY"]

# Logging the Data to the Console
logging.basicConfig(
    # format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    format='# %(message)s',
    level=logging.INFO
)

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        parse_mode=ParseMode.HTML,
        text="Hello,\nI'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type /help to see the list of commands you can use. ")




# Download Videos Function
async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Indetifying the YOUTUBE LINKS from the User Input (message)

    if "youtube.com" in update.message.text or "youtu.be" in update.message.text:
        # await update.message.reply_text("It's a Youtube Link! 😄")
        message = update.message

        for entity in message.entities:
            if entity.type == MessageEntity.URL:
                videoURL = message.parse_entity(entity)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            parse_mode=ParseMode.HTML ,
            text=f"<b>🔗 Given URL:</b><code> {videoURL}</code>")
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            parse_mode=ParseMode.HTML ,
            text=f"Checking your data..")
        


        print("Looking for Available Qualities..")

        # yt = pytube.YouTube(videoURL, on_progress_callback=progressBar.progress_hook)

        # streams = yt.streams.filter(only_video=True, mime_type="video/mp4")
        # mediaPath = f"{os.getcwd()}/vids"

        # # -------VIDEOS-------
        # streamsData = []

        # for count, stream in enumerate(streams, start=1):
        #     # print(f"{count}.  Res: {stream.resolution}  |  Size:{stream.filesize_mb} mb")
        #     # print(stream)
        #     streamsData.append([count, stream.resolution, stream.filesize_mb])

        # # Print the Table of Stream Data
        # print(streamsData)

        # try:
        #     userInput = 3
        #     streams[userInput].download(filename=f"{yt.title}.mp4", output_path=mediaPath)
        #     print("Video Downloaded. ✔")

        # except:
        #     print("Wrong Input! Try Again!")
        #     sys.exit()

        # # -------AUDIOS-------
            
        # for stream in yt.streams.filter(only_audio=True, abr="128kbps"):
        #     stream.download(filename=f"{yt.title}.mp3", output_path=mediaPath)
        #     print("Audio Downloaded. ✔")


        # videoID = pytube.extract.video_id(videoURL)
        # videoFileName = f"{yt.title}_{videoID}.mp4"

        # # Merge the Audio & Video File 
        # vidmerge.merge(title=f"{yt.title}", outVidTitle=videoFileName)

        # # Remove Seperate Media Files
        # os.remove(f"{mediaPath}/{yt.title}.mp4")
        # os.remove(f"{mediaPath}/{yt.title}.mp3")


        # print("Download Completed! ✔")
        # print(f"\nCheck the 'vid' Folder for your files!\n")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            parse_mode=ParseMode.HTML ,
            text=f"<b>Uploading..</b>")
        
        await context.bot.send_document(
            chat_id=update.effective_chat.id, 
            document=open("README.md", "rb"))


# Main Command
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    downloadFilter = filters.TEXT & (filters.Entity("url"))
    application.add_handler(MessageHandler(downloadFilter, download))


    print("-------------------\nBot is Running..\n-------------------")
    application.run_polling()
