import os
import telebot
import threading

from modules import checker, myqueues 

from dotenv import load_dotenv 
load_dotenv()

TOKEN = os.getenv("BOT_API_KEY")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
                      
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, "Hello, I'm a <b>Simple Youtube Downloader!👋</b>\n\nTo get started, just type the /help command.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(
        message,
        """
        <b>Just send your youtube link and select the video quality.</b> 😉
  <i>
  Developer: @dev00111
  Source: <a href="https://github.com/hansanaD/TelegramYTDLBot">TelegramYTDLBot</a></i>
        """, disable_web_page_preview=True,)
        
    

@bot.message_handler(func=lambda m: True)
def link_check(message):
    checker.linkCheck(bot=bot, message=message)
    # print(checker.videoURL)

# Callback handler for # getVidInfo() 
@bot.callback_query_handler(func=lambda call: [call.data == item for item in checker.showList])
def callback_query(call):

    data = call.data.split("#")
    receivedData = data[0]
    videoURL = data[1]
    # print(receivedData)
    
    bot.answer_callback_query(call.id, f"Selected {receivedData} to download.")
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    myqueues.download_queue.put((call.message, videoURL, receivedData))
    queue_position = myqueues.download_queue.qsize()

    
    if queue_position == 0 & 1:
        bot.send_message(call.message.chat.id, f"Download has been added to the queue.")
    else:
        bot.send_message(call.message.chat.id, f"Download has been added to the queue at #{queue_position}.")


    # downloader.download(bot=bot, message=call.message, userInput=receivedData, videoURL=checker.videoURL)
    # bot.send_message(call.message.chat.id, f"{videoURL} \n{receivedData} : Download Triggered!")
            
# message, videoURL, receivedData
    
download_thread = threading.Thread(target=myqueues.download_worker, args=(bot, myqueues.download_queue))
download_thread.daemon = True
download_thread.start()

print("TelegramYTDLBot is running..\n")
bot.infinity_polling()
