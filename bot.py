import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Custom Imports
from telegram import MessageEntity
from telegram.ext import filters, MessageHandler
from telegram.constants import ParseMode
from yt_dlp import YoutubeDL

import os
from dotenv import dotenv_values

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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello,\nI'm a Simple Youtube Downloader!👋\n\nTo get started, just type /help to see the list of commands you can use. ")

# Download Videos Function


async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if "youtube.com" in update.message.text or "youtu.be" in update.message.text:
        # await update.message.reply_text("It's a Youtube Link! 😄")

        message = update.message

        # Iterate over the entities in the message
        for entity in message.entities:
            # Check if the entity is a URL
            if entity.type == MessageEntity.URL:
                # Parse the entity to get the URL text
                videoURL = message.parse_entity(entity)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            parse_mode=ParseMode.HTML ,
            text=f"<b>Checking the Details..</b> 🔗 \n\n URL:<code> {videoURL}</code>")

        ydl_opts = {
            "quiet": True,
            'outtmpl': "%(title)s_%(id)s.%(ext)s",
            # "format": "bestvideo+bestaudio/best",

            # 'progress_hooks': [download_loading_bar],
            'no_color': True,
        }

        print("Fetching the info...")

        with YoutubeDL(ydl_opts) as ydl:
            vidInfo = ydl.extract_info(videoURL, download=False)

            vidTitle = vidInfo.get('title', None)
            vidID = vidInfo.get('id', None)
            vidDuration = vidInfo.get('duration', None)
            vidSize = (vidInfo.get('filesize_approx', None) // 1048576)
            

            print("\n🔹 Title:", vidTitle)
            print("🔹 Duration:", vidDuration)
            print("🔹 Size:", vidSize , "MB")

        print("\nDownloading...")

        ydl.download([videoURL])

        print("Downloaded Successfully! \n ")

        Vidfilename = f"{vidTitle}_{vidID}.mp4"

        # document = open(str(Vidfilename), 'rb')
        # context.bot.send_document(update.effective_chat.id, open(file_path, "rw"))
        await context.bot.send_document(update.effective_chat.id, open(Vidfilename, 'rb'), filename=Vidfilename)
        
        # Delete the file
        os.remove(Vidfilename)


# Main Command
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    downloadFilter = filters.TEXT & (filters.Entity("url"))
    application.add_handler(MessageHandler(downloadFilter, download))

    print("-------------------\nBot is Running..\n-------------------")
    application.run_polling()
