# golestan-grade-checker
Tired of refreshing for grades coming, I decided to write this using Selenium in Python.

### Usage:

You need to first create a `.env` file aside cloned files and enter username and password to your Golestan login page in it using this format:
```
USERNAME=<your username>
PASSWORD=<your password>
```
If you want Telegram notifications, you can add `TOKEN` and `CHAT_ID` pairs which are the token of your bot and the chat id (the numerical id) of your Telegram account, respectively. Also you must set the `tele_notif` to `true` in `config.json` file. (You may want to check [Telegram bots page](https://core.telegram.org/bots) if you're not familiar with them)


If you want SMS notifications, you need to make an account on Kavenegar for free from <a href="https://panel.kavenegar.com/Client/Membership/Register">Here</a>.After that you just need to pick API-KEY up from <a href="http://panel.kavenegar.com/Client/setting/index">My Account</a> section.Then you can add `SMS_KEY` and `PHONE` pairs which are the API-KEY of your kavenegar account and your phone number for receiving SMS notifications to the `.env` file.Also you must set the `sms_notif` to `true` in `config.json` file. (You can check <a href="https://github.com/kavenegar/kavenegar-python">here</a> for more informations)


Then identify which term is the term you are looking for grades coming. You can do it by changing value of `TERM_NO`.

Please note that if you want to use Firefox as the browser (which is as default), you must also have [geckodriver](https://github.com/mozilla/geckodriver/releases) to work with.

Finally, you can run the `main.py` file using `./main.py` or `python3 main.py`.

### Requirements:
* python3.4+
* selenium (For Python)  `pip3 install selenium`
* dotenv (For Python) `pip3 install python-dotenv`
* terminal-notifier (For OSx) `brew install terminal-notifier`
* python-telegram-bot (If you want Telegram notifications, too) `pip3 install python-telegram-bot`
* kavenegar SDK (If you want SMS notifications, too) `pip install kavenegar`

#### Note:
This project sends desktop notifications in Linux Operating System (using `notify-send`) and MacOs (using [`terminal-notifier`](https://github.com/julienXX/terminal-notifier)). It is not tested on Windows and other OSs.
