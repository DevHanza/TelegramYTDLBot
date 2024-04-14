from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
from y2mate_api import Handler


def linkCheck(bot, message):

    linkFilter = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    userLinks = re.findall(linkFilter, message.text)

    yt_link = []
    for link in userLinks:
        if 'youtube.com' in link or 'youtu.be' in link:
            yt_link.append(link)

    if yt_link:
        # bot.reply_to(message, "YouTube links found.")

        # global videoURL
        # global ytApi

        videoURL = yt_link[0]
        

        qualityChecker(bot=bot, message=message, videoURL=videoURL)

    else:
        bot.reply_to(message, "No YouTube links found!")


def qualityChecker(bot, message, videoURL):

    bot.reply_to(message, "Looking for Available Qualities..🔎")

    ytApi = Handler(videoURL)

    q_list = ['4k', '1080p', '720p', '480p', '360p', '240p']
    # q_list.reverse()

    urlList = []

    def getVidInfo(r):
        for video_metadata in ytApi.run(quality=r):
        
            q = video_metadata.get("q")
            dlink = video_metadata.get("dlink")
            size = video_metadata.get("size")
            
            if dlink == None:
                pass
            else:
                urlList.append([q, size, dlink])
                # print(r, " fetched")
                
    # Iterate over q_list to check if res quality exist on that video
    for r in q_list:
        getVidInfo(r)

    # print(urlList)

    # Create a new list to show
    global showList
    showList = {}
    for count, item in enumerate(urlList, 1):
        del item[2] # Remove dlink from list
        q = item[0]
        # print(i)
        size = item[1] 
        showList.update( { count: { "q":q, "size": size }} )
    
    # print(showList)


    # Add Inline Buttons to get user input

    def gen_markup():
        markup = InlineKeyboardMarkup() 
        for value in showList.values(): 
            callbackData = f"{ value["q"] }#{ videoURL }"
            button = InlineKeyboardButton(text=f"{value['q']} ({value['size']})", callback_data=callbackData)
            markup.add(button)
        return markup
 
    bot.reply_to(message=message, text="Choose a stream:", reply_markup=gen_markup())




