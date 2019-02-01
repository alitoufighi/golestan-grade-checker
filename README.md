# golestan-grade-checker
Tired of refreshing for grades coming, I decided to write this using Selenium in Python.

### Usage:

You need to first create a `.env` file aside cloned files and enter username and password to your Golestan login page in it using this format:
```
USERNAME=<your username>
PASSWORD=<your password>
```
If you want Telegram notifications, you can add `TOKEN` and `CHAT_ID` pairs which are the token of your bot and the chat id (the numerical id) of your Telegram account, respectively.

### Requirements:
* python3+
* selenium (For Python)  `pip3 install selenium`
* dotenv (For Python) `pip3 install python-dotenv`
* terminal-notifier (For OSx) `brew install terminal-notifier`
* python-telegram-bot (If you want Telegram notifications, too) `pip3 install python-telegram-bot`

#### Note:
This project sends desktop notifications in Linux Operating System (using `notify-send`) and MacOs (using [`terminal-notifier`](https://github.com/julienXX/terminal-notifier)). It is not tested on Windows and other OSs.
