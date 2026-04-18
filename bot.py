import os, re
import threading
import telebot

from dotenv import load_dotenv

load_dotenv()

from modules.checker import youtube_regex
from modules.downloader import download_video

TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


# '/start' command reply
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Hello, I'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type the /help command.",
    )


# '/help' command reply
@bot.message_handler(commands=["help"])
def send_help(message):
    bot.reply_to(
        message,
        """
        <b>Just send me your video link.</b> ▶️

<i>Source: <a href="https://github.com/hansanaD/TelegramYTDLBot">TelegramYTDLBot</a> by <a href="https://github.com/DevHanza/">DevHanza</a></i>
        """,
        disable_web_page_preview=True,
    )


# Youtube Link Listener
@bot.message_handler(func=lambda m: True)
def on_yt_link(message):
    # run download in background so bot stays responsive
    threading.Thread(target=yt_link_handler, args=(message,)).start()


def yt_link_handler(message):

    matches = re.findall(youtube_regex, message.text)

    if matches:

        url = matches[0]
        status_msg = bot.reply_to(message, f"Starting to download..")

        try:
            file_path = download_video(url, bot, message.chat.id, status_msg.message_id)

            with open(file_path, "rb") as file:
                bot.send_video(message.chat.id, file)

            os.remove(file_path)

        except Exception as e:
            bot.reply_to(message, f"❌ Error: {e}")


print("TelegramYTDLBot is running..\n")
bot.infinity_polling()
