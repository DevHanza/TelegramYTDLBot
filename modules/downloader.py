from yt_dlp import YoutubeDL

from modules.progress import create_progress_bar


def download_video(url: str, bot, chat_id: int, message_id: int) -> str:
    options = {
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",
        "noplaylist": True,
        "quiet": False,
        "merge_output_format": "mp4",
        "progress_hooks": [create_progress_bar(bot, chat_id, message_id)],
    }

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return filename

    except Exception as e:
        print(f"Error downloading video: {e} ❌")
