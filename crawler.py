from selenium import webdriver
import os
import time

# Constants
LOGIN_URL = 'https://signin.intra.42.fr/users/sign_in'
PROJECT_URL = 'https://projects.intra.42.fr/projects/list'

# Load Chrome Driver
prefs = {"plugins.always_open_pdf_externally": True, "plugins.plugins_disabled": ["Chrome PDF Viewer"]}
options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('./chromedriver', options=options)

# Login
driver.get(LOGIN_URL)
driver.find_element_by_xpath('//*[@id="user_login"]').send_keys('id') # id
driver.find_element_by_xpath('//*[@id="user_password"]').send_keys('password') # password
driver.find_element_by_xpath('//*[@id="new_user"]/div[2]/input').click()
driver.get(PROJECT_URL)

# Collect project links
links = driver.find_elements_by_class_name('project-name')
link_list = []
for link in links:
    link = link.find_element_by_tag_name('a').get_attribute('href')
    link_list.append(link)
os.system("rm ~/Downloads/en.subject*")

# Iterate each link
for link in link_list:
    try:
        driver.get(link)
        item = driver.find_element_by_class_name('project-attachment-item')
        project_name = link.split('/')[-1]
        link = item.find_element_by_tag_name('a').get_attribute('href')
        driver.get(link)
        time.sleep(1.5)
        print(link)
        print(project_name)
        os.system('mv ~/Downloads/en.subject.pdf ' + '~/goinfre/' + project_name)
    except:
        pass
    time.sleep(1)
driver.close()
