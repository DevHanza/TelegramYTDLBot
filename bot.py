import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Custom Imports
# from telegram import 
from telegram.ext import filters, MessageHandler


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
        await update.message.reply_text("It's a Youtube Link! 😄")

        
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I have detected a link. 🔗")
    
    



    
# Main Command
if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    
    downloadFilter = filters.TEXT & (filters.Entity("url"))
    application.add_handler(MessageHandler(downloadFilter, download))

    print("-------------------\nBot is Running..\n-------------------")
    application.run_polling()
