# YouTube Downloader Bot
A Simple Telegram Bot to Download YouTube Videos. (Only for Educational Purposes)

#
### 1. Setup Environment Variables
- Get your [BOT_API_KEY](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) from here.
- Create .env file
- Paste this code into your file and replace with your own values.
```
BOT_API_KEY = "6357576507:AAHePL8-xSzjOlnF5dRGiwhNyxxZsS3u7f4" # Replace with your own token
```
- Save it!
  
#
### 2. Install Dependencies
```
git clone https://github.com/hansanaD/TelegramYTDLBot.git;
cd TelegramYTDLBot;
pip install -r requirements.txt;
python bot.py
```
#
### 3. Run api server locally (optional)
You can choose not to use this service.\
But then you won't be able  to **upload files up to 2000 MB** and get these [features](https://core.telegram.org/bots/api#using-a-local-bot-api-server).

- Read the instructions on [tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api) first.
- Now run these commands,
- Go to: ```cd telegram-bot-api/bin```
- Get [API ID & API HASH](https://core.telegram.org/api/obtaining_api_id)
- Start the server by replacing the api-id and api-hash on here,
- ``` ./telegram-bot-api --api-id=XXXXX --api-hash=XXXXXXXXXXXX --http-port=8081 --local ```
#
### 4. Run your bot
- open a new "[screen](https://www.geeksforgeeks.org/screen-command-in-linux-with-examples/)" or tab on your terminal.
- run: ``` python bot.py```

**both script & api server should run at the same time order to work.**
#
_Sorry for my bad english and my messy documentation. 😶_



  


