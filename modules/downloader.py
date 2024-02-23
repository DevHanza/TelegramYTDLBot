import os
from y2mate_api import Handler

# Download the YouTube Video
def download(bot, message, userInput, videoURL):
    api = Handler(videoURL)

    mediaPath = f"{os.getcwd()}/vids"

    # Download the video using user's input
    for video_metadata in api.run(quality=userInput):
        # print(video_metadata)
        
        if not os.path.exists(mediaPath):
            os.makedirs(mediaPath)

        bot.send_message(message.chat.id, f"Downloading..")
        api.save(third_dict=video_metadata, dir="vids", progress_bar=True)

        vidFileName = f"{video_metadata["title"]} {video_metadata["vid"]}_{video_metadata["fquality"]}.{video_metadata["ftype"]}"
    
        bot.send_message(message.chat.id, f"Downloaded.")

        # Upload the video to Telegram
        with open(f"vids/{vidFileName}", 'rb') as file:
            bot.send_document(message.chat.id, file)
        print("File was uploaded/sent to the User.")

        bot.send_message(message.chat.id, f"File deleted from the database.")
        os.remove(f"{mediaPath}/{vidFileName}")
   