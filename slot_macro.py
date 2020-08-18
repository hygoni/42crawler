from selenium import webdriver
import os
import time
from getpass import getpass
import time as t

# Constants
LOGIN_URL = 'https://signin.intra.42.fr/users/sign_in'
PROJECT_URL = 'https://projects.intra.42.fr/projects/list'

# Load Chrome Driver
prefs = {"plugins.always_open_pdf_externally": True, "plugins.plugins_disabled": ["Chrome PDF Viewer"]}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('./chromedriver', options=options)

login = input('id : ')
password = getpass()

# Login
driver.get(LOGIN_URL)
driver.find_element_by_xpath('//*[@id="user_login"]').send_keys(login) # id
driver.find_element_by_xpath('//*[@id="user_password"]').send_keys(password) # password
driver.find_element_by_xpath('//*[@id="new_user"]/div[2]/input').click()

# Input slot page URL
URL = input('input slot URL : ')

# select day of week
WEEK_DAY = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
print('week_days = ', WEEK_DAY)
select_week_day = input('select week day : ')
driver.get(URL)
idx = WEEK_DAY.index(select_week_day)


# 5:00 PM - 6:00 PM

#time = '5:00 PM'
def convert_time(time):
    time = time.upper()
    time, ap = time.split(' ')
    hour, minute = time.split(':')
    hour = int(hour)
    minute = int(minute)
    time = 60 * hour + minute
    if ap == 'PM':
        time += 12 * 60
    return time

print('time format : H:M PM or H:M AM')
start_time = convert_time(input('start time : '))
end_time = convert_time(input('end time : '))

t.sleep(3)
while True:
    columns = driver.find_elements_by_class_name('fc-content-col')
    for slot in columns[idx].find_elements_by_class_name('fc-time'):
        times = slot.get_attribute('data-full').split(' - ')
        times = [convert_time(time) for time in times]
        if start_time <= times[0] and times[1] <= end_time:
            slot.click()
            exit() 
    driver.get(URL)
    time.sleep(3)
driver.close()
