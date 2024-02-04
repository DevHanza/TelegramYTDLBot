# Import the required modules
import telebot
import yt_dlp
import os

# Create a bot instance with your token
bot = telebot.TeleBot("6357576507:AAHcfnIFNHtmv-4aqoFbGsuDw_vsxBZgTnE")

# Define a handler for /start command
@bot.message_handler(commands=["start"])
def start(message):
    # Send a welcome message
    bot.send_message(message.chat.id, "Hello, I am a bot that can download YouTube videos for you. Send me a YouTube URL and I will show you the available formats.")

# Define a handler for YouTube URLs
@bot.message_handler(regexp=r"https?://(www\.)?youtube\.com/watch\?v=\w+")
def youtube(message):
    # Extract the video ID from the URL
    video_id = message.text.split("v=")[-1]
    # Create a yt-dlp instance
    ydl = yt_dlp.YoutubeDL({"format": "bestvideo+bestaudio/best", "noplaylist": True})
    # Get the video info
    info = ydl.extract_info(video_id, download=False)
    # Get the title and thumbnail
    title = info["title"]
    thumb = info["thumbnail"]
    # Get the available formats
    formats = info["formats"]
    # Create a list of buttons for each format
    buttons = []
    for f in formats:
        # Get the format ID, extension, resolution and filesize
        fid = f["format_id"]
        ext = f["ext"]
        res = f.get("height", "audio only")
        size = f.get("filesize")
        # Format the button text
        text = f"{fid} ({ext}) - {res}p"
        if size:
            text += f" - {round(size / (1024 ** 2), 2)} MB"
        # Create a callback data with the video ID and format ID
        data = f"{video_id}|{fid}"
        # Append the button to the list
        buttons.append([telebot.types.InlineKeyboardButton(text, callback_data=data)])
    # Create an inline keyboard with the buttons
    keyboard = telebot.types.InlineKeyboardMarkup(buttons)
    # Send the video title, thumbnail and keyboard
    bot.send_photo(message.chat.id, thumb, caption=title, reply_markup=keyboard)

# Define a handler for callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # Acknowledge the callback
    bot.answer_callback_query(call.id)
    # Get the video ID and format ID from the callback data
    video_id, format_id = call.data.split("|")
    # Create a yt-dlp instance with the desired format and output template
    ydl = yt_dlp.YoutubeDL({"format": format_id, "outtmpl": f"{video_id}_{format_id}.%(ext)s"})
    # Download the video
    ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
    # Get the output filename
    filename = ydl.prepare_filename(ydl.extract_info(video_id, download=False))
    # Send the video file
    bot.send_document(call.message.chat.id, open(filename, "rb"))
    # Delete the file
    os.remove(filename)


    # Start polling
bot.polling()

