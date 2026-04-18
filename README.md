# <p align="center">TelegramYTDLBot</p>

<p align="center">A Telegram Bot to Download YouTube videos in the highest quality possible under 2GB.</p>
<p align="center"><i>Only for Educational Purposes.</i></p>

## Features

- ✅ Fast & High quality downloads.
- ✅ Max video upload size : 2GB
- ✅ Fewer dependencies
- ✅ Docker deployment

## How to Deploy

### Docker

```bash
docker build -t telegram-ytdl-bot .
docker run --env-file .env telegram-ytdl-bot
```

### Python

```bash
git clone https://github.com/hansanaD/TelegramYTDLBot.git;
cd TelegramYTDLBot;
pip install -r requirements.txt;
```

#### Setup Environment VariablesInstallation

- Rename the `.exmaple.env` to `.env` and update its values. Instructions can be found as comments in the .env file.

#### Run api server locally (optional)

You can choose not to use this service.\
But then you won't be able to **upload files up to 2000 MB** and get these [features](https://core.telegram.org/bots/api#using-a-local-bot-api-server).

- Generate your instructions from [here](https://tdlib.github.io/telegram-bot-api/build.html). _(This step might take upto 20 mins.)_
- Go to:
- ```
  cd telegram-bot-api/bin
  ```
- Get API ID & HASH from [here](https://core.telegram.org/api/obtaining_api_id). (Watch this [Tutorial](https://www.youtube.com/watch?v=8naENmP3rg4) to get help.)
- Start the server. (Remember to replace the values with your own values):
- ```
  ./telegram-bot-api --api-id=XXXXX --api-hash=XXXXXXXXXXXX --http-port=8081 --local
  ```

Read the instructions on [eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/#using-local-bot-api-sever) and [tdlib/telegram-bot-api](https://github.com/tdlib/telegram-bot-api) for more information.

#### Run your bot

Open a new "[screen](https://www.geeksforgeeks.org/screen-command-in-linux-with-examples/)" or tab on your terminal. Then run:

```bash
python bot.py
```

**both the script & api server should run at the same time order to work.**

## Dependencies

- [pytelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Disclaimer

This repository is intended for educational and personal use only. The use of this repository for any commercial or illegal purposes is strictly prohibited. The repository owner does not endorse or encourage the downloading or sharing of copyrighted material without permission. The repository owner is not responsible for any misuse of the software or any legal consequences that may arise from such misuse
