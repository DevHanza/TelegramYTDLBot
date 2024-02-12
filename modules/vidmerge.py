
import os
import ffmpeg


def merge(title, outVidTitle):

    input_video = os.path.join(os.getcwd(), "vids",f"{title}.mp4")  
    input_audio = os.path.join(os.getcwd(), "vids",f"{title}.mp3")  

    f_vid = ffmpeg.input(input_video)
    f_aud = ffmpeg.input(input_audio)

    # Delete the video if it already exist.
    if os.path.exists(f"vids/{outVidTitle}"):
        os.remove(f"vids/{outVidTitle}")

    ffmpeg.concat(f_vid, f_aud, v=1, a=1).output(f"vids/{outVidTitle}").run()

