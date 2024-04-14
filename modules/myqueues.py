import time
from queue import Queue
from modules.ytdownloader import download

download_queue = Queue()

def download_worker(bot, download_queue):
    while True:
        message, videoURL, receivedData = download_queue.get()
        try:
            download(bot=bot, message=message, userInput=receivedData, videoURL=videoURL)

        except Exception as e:
            print(f"Error downloading file: {e}")
        download_queue.task_done()

        # Check if the queue is empty
        if download_queue.empty():
            print("All downloads have been completed. Queue is empty now.\n\n")


