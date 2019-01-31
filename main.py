import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only
from time import sleep
from selenium import webdriver
import subprocess as s
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

TERM_NO = 5  # Which term are you in?

# University of Tehran CAS Url (Change to yours, if you aren't UT student)
UTCAS_URL = "https://auth4.ut.ac.ir:8443/cas/login?service=https://ems1.ut.ac.ir/forms/casauthenticateuser/\
casmu.aspx?ut=1%26CSURL=https://auth4.ut.ac.ir:8443/cas/logout?service$https://ems.ut.ac.ir/"

s.call(['notify-send', 'Golestan Grade Checker is running', 'By Ali_Tou'])

# We used dotenv module to handle username and password security.
load_dotenv(verbose=True)
env_path = Path('./env') / '.env'
load_dotenv(dotenv_path=str(env_path))

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.tabs.remote.autostart", False)
fp.set_preference("browser.tabs.remote.autostart.1", False)
fp.set_preference("browser.tabs.remote.autostart.2", False)

driver = webdriver.Firefox(fp)


def switch_to_grades_frame(Faci_id):
    switch_to_main_frame(Faci_id)
    frame = driver.find_element_by_xpath('/html/body')
    frame = frame.find_element_by_xpath(""".//iframe[@id="FrameNewForm"]""")
    driver.switch_to.frame(frame)


def switch_to_main_frame(Faci_id):
    WebDriverWait(driver, 50)\
        .until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, f"""//*[@id="Faci{Faci_id}"]""")))
    frame = driver.find_element_by_xpath('/html/frameset/frameset/frame[2]')
    driver.switch_to.frame(frame)
    frame = driver.find_element_by_xpath('/html/frameset/frame[3]')
    driver.switch_to.frame(frame)


# Login to Golestan
driver.get(UTCAS_URL)
username_field = driver.find_element_by_xpath("""//input[@id="usename-field"]""")
password_field = driver.find_element_by_xpath("""//input[@id="password"]""")
username_field.send_keys(USERNAME)
password_field.send_keys(PASSWORD)
password_field.send_keys(Keys.ENTER)


# Golestan uses frames. To access main body of page, we need to switch between its frames
sleep(30)
switch_to_main_frame(2)
sleep(5)

etelaate_jame_daneshjoo = driver.find_element_by_xpath("""//*[text()='اطلاعات جامع دانشجو']""")
etelaate_jame_daneshjoo.click()
sleep(1.5)
etelaate_jame_daneshjoo.click()

# now we are in اطلاعات جامع دانشجو Page
# So we go to dedicated term page
sleep(7)
driver.switch_to.default_content()
switch_to_main_frame(3)
terms_status_table = driver.find_element_by_xpath("""//table[@id="T01"]""")
term_field = terms_status_table.find_element_by_xpath(f"""//tr[@class="TableDataRow"][{TERM_NO}]/td[1]""")
term_field.click()


sleep(7)
# Finally, we're in our desired term page
driver.switch_to.default_content()
switch_to_grades_frame(3)
sleep(0.5)


def find_given_grades():
    result = 0
    grades_table = driver.find_element_by_xpath(""".//table[@id="T02"]""")
    grades_table = grades_table.find_element_by_xpath(""".//tbody""")
    grades_rows = grades_table.find_elements_by_xpath(""".//tr[@class="TableDataRow"]""")

    print("Given Grades are:")
    for row in grades_rows:
        row_text = row.find_element_by_xpath(""".//td[9]""")
        grade = row_text.find_element_by_xpath(""".//nobr[1]""").text
        if grade != "":
            print(grade)
            result += 1
    return result


previous_grades = -1
while True:
    given_grades = find_given_grades()
    if previous_grades != -1 and previous_grades != given_grades:
        s.call(['notify-send', 'Golestan Grade Checker', 'You have new grades in golestan!'])
    previous_grades = given_grades
    print(f"Given Grades are {given_grades}")

    # give professors some time to enter our grades -__-
    sleep(180)

    # Preventing Golestan to log us out because of inactivity by clicking on previous term and next term.
    # This doesn't work when you're a freshman (When you don'y have any previous term)
    previous_term = driver.find_element_by_xpath(""".//img[@title="ترم قبلي"]""")
    previous_term.click()
    sleep(8)
    driver.switch_to.default_content()
    switch_to_grades_frame(3)
    next_term = driver.find_element_by_xpath(""".//img[@title="ترم بعدي"]""")
    next_term.click()
