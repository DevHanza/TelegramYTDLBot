import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

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



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    print("-------------------\nBot is Running..\n-------------------")
    application.run_polling()