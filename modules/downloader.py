import os
from y2mate_api import Handler
import requests

# Download the YouTube Video
async def download(bot, yt, message, userInput, videoURL, loadingMsg, ytThumbMsg):
    api = Handler(videoURL)

    mediaPath = f"{os.getcwd()}/vids"

    # Download the video using user's input
    for video_metadata in api.run(quality=userInput):
        # print(video_metadata)
        
        if not os.path.exists(mediaPath):
            os.makedirs(mediaPath)

        await bot.edit_message_text(chat_id=message.chat.id, message_id=loadingMsg.message_id, text="<b>Downloading...📥</b>")

        vidFileName = f"{ video_metadata['vid'] }_{ video_metadata['q'] }.{ video_metadata['ftype'] }"

        # Start Downloading the Video
        api.save(third_dict=video_metadata, dir="vids", naming_format=vidFileName, progress_bar=True)

    
        await bot.edit_message_text(chat_id=message.chat.id, message_id=loadingMsg.message_id, text="<b>Uploading...📤</b>")

        # Upload the video to Telegram
        try:
            print(vidFileName, "Uploading..")
            await bot.send_video(
                message.chat.id, 
                open(f"vids/{vidFileName}", 'rb'), 
                thumb=requests.get(yt.thumbnail_url).content,
                # caption= f" <i>Thanks for Using @{bot.get_me().username }.</i> ", 
                width=1920, 
                height=1080,
                caption=f"""
                <b>Title:</b><i> { yt.title } </i>
<b>URL:</b><i> { videoURL } </i>
<b>Quality:</b><i> { video_metadata['q'] } </i>

<i><b>Thanks for Using @YoutubeDownloader4K0_bot.</b></i>""",
            )

            print("File was uploaded/sent to the User.")
            os.remove(f"{mediaPath}/{vidFileName}")

        except Exception as e:
            await bot.reply_to(message, f"Error uploading video: {e}")
    
        # Delete ytThumbMsg after video upload done.
        await bot.delete_message(chat_id=message.chat.id, message_id=ytThumbMsg.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=loadingMsg.message_id)

        
