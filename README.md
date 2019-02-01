# golestan-grade-checker
Tired of refreshing for grades coming, I decided to write this using Selenium in Python.

Usage:

You need to first create a `.env` file aside cloned files and enter username and password to your Golestan login page in it using this format:
```
USERNAME=<your username>
PASSWORD=<your password>
```

# Requirements:
* Python3+
* Selenium (For Python)  `pip3 install selenium`
* Dotenv (For Python) `pip3 install python-dotenv`
* terminal-notifier (For OSx) `brew install terminal-notifier`

Note: This project sends desktop notifications in Linux Operating System (using `notify-send`) and MacOs (using [`terminal-notifier`](https://github.com/julienXX/terminal-notifier)). It is not tested on Windows and other OSs.
