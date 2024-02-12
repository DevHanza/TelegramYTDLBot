import telebot , re, pytube , os , sys
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

bot = telebot.TeleBot(TOKEN, parse_mode="MARKDOWN") # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello, I'm a *Simple Youtube Downloader!👋*\n\nTo get started, just type the /help command.")
	
@bot.message_handler(func=lambda m: True)
def download(message):

# Indetifying the YOUTUBE LINKS from the User Input (message)

    # Use a regular expression to find all URLs in the text
    all_links = re.findall(r'(https?://[^\s]+)', message.text)

    # Filter out the URLs that are not YouTube links
    youtube_links = []
    for link in all_links:
        if 'youtube.com' in link or 'youtu.be' in link:
            youtube_links.append(link)

    # Check if any YouTube links were found
    if youtube_links:
        # bot.reply_to(message, f"Found YouTube links: {', '.join(youtube_links)}")
        bot.reply_to(message, f"Found YouTube links: {', '.join(youtube_links)}")

        if len(youtube_links) > 1:
            bot.reply_to(message, "By sending multiple links at once, *only the first link* will be downloaded!.")
        
        videoURL = youtube_links[0]
    else:
        bot.reply_to(message, "No YouTube links found.")

# Download the video from YouTube using pytube
        
    print("Looking for Available Qualities..")
    bot.reply_to(message, "Looking for Available Qualities..")

    yt = pytube.YouTube(videoURL, on_progress_callback=progressBar.progress_hook)

    streams = yt.streams.filter(only_video=True, mime_type="video/mp4")
    mediaPath = f"{os.getcwd()}/vids"

    # -------VIDEOS-------

    streamsData = []

    for count, stream in enumerate(streams, start=1):
        # print(f"{count}.  Res: {stream.resolution}  |  Size:{stream.filesize_mb} mb")
        # print(stream)
        streamsData.append([count, stream.resolution, stream.filesize_mb])

    # Print the Table of Stream Data
    print(streamsData)

    try:
        userInput = 3
        streams[userInput].download(filename=f"{yt.title}.mp4", output_path=mediaPath)
        print("Video Downloaded. ✔")

    except:
        print("Wrong Input! Try Again!")
        sys.exit()

    # -------AUDIOS-------
            
    for stream in yt.streams.filter(only_audio=True, abr="128kbps"):
        stream.download(filename=f"{yt.title}.mp3", output_path=mediaPath)
        print("Audio Downloaded. ✔")


    videoID = pytube.extract.video_id(videoURL)
    videoFileName = f"{yt.title}_{videoID}.mp4"

    # Merge the Audio & Video File 
    vidmerge.merge(title=f"{yt.title}", outVidTitle=videoFileName)

    bot.reply_to(message, "Uploading...")

    with open(f"vids/{videoFileName}", 'rb') as file:
        bot.send_document(message.chat.id, file)

    bot.reply_to(message, "Downloaded.")
    


    # Remove the Media Files
    os.remove(f"{mediaPath}/{yt.title}.mp4")
    os.remove(f"{mediaPath}/{yt.title}.mp3")
    os.remove(f"{mediaPath}/{videoFileName}")
    print("File was sent to User & Deleted from local.")

print("TelegramYTDLBot is running..")
bot.infinity_polling()