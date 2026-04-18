import time


def progress_bar(percent, length=20):
    filled = int(length * percent // 100)
    return "█" * filled + "░" * (length - filled)


def create_progress_bar(bot, chat_id, message_id):
    """
    Returns a yt-dlp progress hook function
    that updates a Telegram message.
    """
    last_update_time = 0

    def hook(d):
        nonlocal last_update_time

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)

            if total:
                percent = downloaded / total * 100

                # throttle edits to avoid Telegram limits
                if time.time() - last_update_time > 2:
                    bar = progress_bar(percent)

                    text = f"Downloading...\n" f"[{bar}] {percent:.1f}%"

                    try:
                        bot.edit_message_text(text, chat_id, message_id)
                    except Exception:
                        pass

                    last_update_time = time.time()

        elif d["status"] == "finished":
            try:
                bot.edit_message_text("Uploading...", chat_id, message_id)
            except Exception:
                pass

    return hook
