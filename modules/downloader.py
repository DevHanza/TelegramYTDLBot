import os
from y2mate_api import Handler

# Download the YouTube Video
def download(bot, message, userInput, videoURL, loadingMsg):
    api = Handler(videoURL)

    mediaPath = f"{os.getcwd()}/vids"

    # Download the video using user's input
    for video_metadata in api.run(quality=userInput):
        # print(video_metadata)
        
        if not os.path.exists(mediaPath):
            os.makedirs(mediaPath)

        bot.edit_message_text(chat_id=message.chat.id, message_id=loadingMsg.message_id, text="<b>Downloading...📥</b>")

        # Start Downloading the Video
        api.save(third_dict=video_metadata, dir="vids", progress_bar=True)

        vidFileName = f"{video_metadata["title"]} {video_metadata["vid"]}_{video_metadata["fquality"]}.{video_metadata["ftype"]}"
    
        bot.edit_message_text(chat_id=message.chat.id, message_id=loadingMsg.message_id, text="<b>Uploading...📤</b>")

        # Upload the video to Telegram
        with open(f"vids/{vidFileName}", 'rb') as file:
            bot.send_document(message.chat.id, file, caption= f" <i>Thanks for Using @{bot.get_me().username }.</i> ")
        print("File was uploaded/sent to the User.")

        bot.delete_message(chat_id=message.chat.id, message_id=loadingMsg.message_id)

        os.remove(f"{mediaPath}/{vidFileName}")
   