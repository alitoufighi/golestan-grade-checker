#!/usr/bin/python3

import os
import platform
from dotenv import load_dotenv
from pathlib import Path
from time import sleep
from selenium import webdriver
import subprocess as s
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from telegram.ext import Updater

TERM_NO = 5  # Which term are you in?
TELEGRAM_NOTIF = True

# University of Tehran CAS Url (Change to yours, if you are not a UT student)
UTCAS_URL = "https://auth4.ut.ac.ir:8443/cas/login?service=https://ems1.ut.ac.ir/forms/casauthenticateuser/\
casmu.aspx?ut=1%26CSURL=https://auth4.ut.ac.ir:8443/cas/logout?service$https://ems.ut.ac.ir/"

OS = 'OSx' if platform.system() == 'Darwin' else 'Linux'

def mac_notify(title, subtitle, message , sound_on):
    title = '-title {!r}'.format(title)
    sub = '-subtitle {!r}'.format(subtitle)
    msg = '-message {!r}'.format(message)
    sound = '-sound default' if sound_on else ''
    os.system('terminal-notifier {}'.format(' '.join([msg, title, sub, sound])))


if(OS is 'OSx'):
    mac_notify("Golestan", 'By Ali_Tou', 'Golestan Grade Checker is running', sound_on = False)
else:
    s.call(['notify-send', 'Golestan Grade Checker is running', 'By Ali_Tou'])


# dotenv is used to handle username and password security.
load_dotenv(verbose=True)
env_path = Path('./env') / '.env'
load_dotenv(dotenv_path=str(env_path))

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# setup Firefox profile (you can use other browsers, but I prefer Firefox)
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.tabs.remote.autostart", False)
fp.set_preference("browser.tabs.remote.autostart.1", False)
fp.set_preference("browser.tabs.remote.autostart.2", False)

driver = webdriver.Firefox(fp)
updater = None
if TELEGRAM_NOTIF:
    updater = Updater(TOKEN)


def switch_to_grades_frame(faci_id):
    """
    Golestan uses frames. To access main body of page, we need to switch between its frames
    :param faci_id: Golestan frames has a Faci_id which is the id of that frame.
            According to our usage, we need to navigate to different Faci_ids.
    """
    switch_to_main_frame(faci_id)
    frame = driver.find_element_by_xpath('/html/body')
    frame = frame.find_element_by_xpath(""".//iframe[@id="FrameNewForm"]""")
    driver.switch_to.frame(frame)


def switch_to_main_frame(faci_id):
    WebDriverWait(driver, 50)\
        .until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, f"""//*[@id="Faci{faci_id}"]""")))
    frame = driver.find_element_by_xpath('/html/frameset/frameset/frame[2]')
    driver.switch_to.frame(frame)
    frame = driver.find_element_by_xpath('/html/frameset/frame[3]')
    driver.switch_to.frame(frame)


def login_to_golestan(login_url, username, password):
    """
    Logs into Golestan system.
    You may need to change xpath of username and password fields if according to your university login web page.
    :param login_url: Main URL of logging into your Golestan system
    :param username: Your username to Golestan
    :param password: Your password to Golestan
    """
    driver.get(login_url)
    username_field = driver.find_element_by_xpath("""//input[@id="usename-field"]""")
    password_field = driver.find_element_by_xpath("""//input[@id="password"]""")
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)


def go_to_etelaate_jame_daneshjoo_page():
    """
    From golestan main page, it navigates to Etelaate Jame-e Daneshjoo page
    """
    switch_to_main_frame(2)
    sleep(5)
    etelaate_jame_daneshjoo_button = driver.find_element_by_xpath("""//*[text()='اطلاعات جامع دانشجو']""")
    etelaate_jame_daneshjoo_button.click()
    sleep(1)
    etelaate_jame_daneshjoo_button.click()


def go_to_semester(term_no):
    """
    From Etelaate Jame-e Daneshjoo, it navigates to your dedicated term page
    :param term_no: Which term are you going to check your grades?
    """
    driver.switch_to.default_content()
    switch_to_main_frame(3)

    terms_status_table = driver.find_element_by_xpath("""//table[@id="T01"]""")
    term_field = terms_status_table.find_element_by_xpath(f"""//tr[@class="TableDataRow"][{term_no}]/td[1]""")
    term_field.click()


def find_given_grades():
    result = {}
    grades_table = driver.find_element_by_xpath(""".//table[@id="T02"]""")
    grades_table = grades_table.find_element_by_xpath(""".//tbody""")
    grades_rows = grades_table.find_elements_by_xpath(""".//tr[@class="TableDataRow"]""")
    print("Your given Grades are:")
    for row in grades_rows:
        course_name = row.find_element_by_xpath(""".//td[6]""").get_attribute("title")
        grade_element = row.find_element_by_xpath(""".//td[9]""")
        course_grade = grade_element.find_element_by_xpath(""".//nobr[1]""").text
        if course_grade != "":
            print(course_name, course_grade)
            result[course_name] = course_grade
    return result


def refresh_grades_page():
    """
    This is dummy!
    Preventing Golestan to log us out because of inactivity, by clicking on previous term and next term.
    NOTE: This doesn't work when you're a freshman (When you don'y have any previous term)
        (Subject to change if another solution is found)
    """
    previous_term = driver.find_element_by_xpath(""".//img[@title="ترم قبلي"]""")
    previous_term.click()
    sleep(5)
    driver.switch_to.default_content()
    switch_to_grades_frame(3)
    next_term = driver.find_element_by_xpath(""".//img[@title="ترم بعدي"]""")
    next_term.click()
    sleep(5)


login_to_golestan(UTCAS_URL, USERNAME, PASSWORD)
sleep(20)
go_to_etelaate_jame_daneshjoo_page()
sleep(7)
go_to_semester(TERM_NO)
sleep(7)

driver.switch_to.default_content()
switch_to_grades_frame(3)
sleep(0.5)

previous_grades = -1  # it will be changed to dictionary later


def create_grades_message(grades):
    """
    Takes a list of tuples of grades in format (NAME, GRADE) and returns a beautified string
    :param grades: a list of tuples of grades
    :return: beautified string of grades with names and marks
    """
    result = ""
    for grade in grades:
        # result += name + ": " + grade
        result += f"{', '.join(grade)}"


while True:
    given_grades = find_given_grades()
    if previous_grades != -1 and previous_grades != given_grades:
        diff = list(set(given_grades.items()) ^ set(previous_grades.items()))
        new_grades_message = create_grades_message(diff)
        # Print on console
        print('You have new grades!')
        print(diff)
        print('---------')

        if(OS is 'Osx'):
            mac_notify("Golestan", 'Golestan Grade Checker', 'You have new grades in golestan!', sound_on = True)
        else:
            # Play a beep sound (using sox)
            s.call(['play', '--no-show-progress', '--null', '-t', 'alsa', '--channels', '1', 'synth', '1', 'sine', '330'])

            # Send a desktop notification (using notify-send)
            s.call(['notify-send', 'Golestan Grade Checker', 'You have new grades in golestan!'])

    previous_grades = given_grades
    print(f"Given Grades are {given_grades}")
    if TELEGRAM_NOTIF: 
        updater.bot.send_message(chat_id = CHAT_ID,
                                 text = str(f"Given Grades are {given_grades}"))

    print(f"Number of given Grades: {given_grades}")

    # give professors some time to insert our grades -__-
    sleep(180)

    refresh_grades_page()
