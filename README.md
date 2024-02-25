# YouTube Downloader Bot
A Simple Telegram Bot to Download YouTube Videos. (Only for Educational Purposes)


### 1. Setup Environment Variables
- [BotToken](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)
- [API ID & API HASH](https://core.telegram.org/api/obtaining_api_id)
  
Please update the values in the `.env` file before run it on anywhere.

### 2. Install Dependencies
```
git clone https://github.com/hansanaD/TelegramYTDLBot.git;
cd TelegramYTDLBot;
pip install -r requirements.txt;
python bot.py
```
### 3. Run your telegram bot api server locally

- Read the instructions on [tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api) first.
- Now run these commands,
- Go to: ```cd telegram-bot-api/bin```
- Start the server by replace the api-id and api-hash on here,
- ``` ./telegram-bot-api --api-id=XXXXX --api-hash=XXXXXXXXXXXX --local ```

### 4. Run your script (ex: bot.py)
- open a new "screen" or tab on your terminal.
- run: ``` python bot.py```

**both script & api server should run at the same time order to work.**

_Sorry for my bad english and my messy documentation. 😶_



  


