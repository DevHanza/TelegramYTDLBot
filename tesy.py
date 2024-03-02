"""
from collections import deque

dQueue = deque({})

dQueue.append({ "userID" : 123456, "URL": "XXXXXX" })
dQueue.append({ "userID" : 456, "URL": "XXXXXX" })

print(dQueue[0])
deque.popleft()
print(dQueue[0])

"""

import telebot
from collections import deque

import threading , time #
from y2mate_api import Handler


TOKEN = "6357576507:AAHGMlOvC9VZuYDptZQt_pXFHM2SLTTmeBc"
bot = telebot.TeleBot(TOKEN, threaded=True)
# from telebot.async_telebot import AsyncTeleBot
# bot = AsyncTeleBot(TOKEN)

dQueue = deque({})


def nextProcess():

    # api = Handler(f"{dQueue[0]["URL"]}")
    # api.auto_save()

    api = Handler({dQueue[0]["URL"]})
    for video_metadata in api.run():
        vidFileName = f"{ video_metadata['vid'] }_{ video_metadata['q'] }.{ video_metadata['ftype'] }"
        api.save(third_dict=video_metadata, naming_format=vidFileName)
        
        bot.send_video(dQueue[0]["chatID"], open(f"{vidFileName}", 'rb'))
    
    bot.send_message(dQueue[0]["chatID"], "Process finished. : ", {dQueue[0]["URL"]} )
    dQueue.popleft()
        

@bot.message_handler(func=lambda message: True)
def getURL(message):

    print(dQueue)
    bot.send_message(message.chat.id, "Your Process added to the queue.")

    dQueue.append( { "chatID" : message.chat.id, "URL": message.text } )
    nextProcess()


print("Running..")
bot.infinity_polling()










