import telebot
# from telebot import apihelper
from dotenv import dotenv_values

EnvConfig = dotenv_values(".env")
TOKEN = EnvConfig["BOT_API_KEY"]

# apihelper.API_URL = "http://0.0.0.0:8081/bot{0}/{1}"
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


a = bot.log_out()
print("Logged out?:", a)