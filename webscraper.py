# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 14:21:56 2024

@author: arjun
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import time

#%%
# set up a controllable Chrome instance
# in headless mode
service = Service()
options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
driver = webdriver.Chrome(
    service=service,
    options=options
)

actions = ActionChains(driver)

# set the window size to make sure pages
# will not be rendered in responsive mode
#driver.set_window_size(1920, 1080)

# open the target page  in the browser
driver.get("https://europa.eu/europass/en/find-jobs?keyword=data&location=Germany&order=relevance&form_build_id=form-Kwm_IYWWCd_v29y--AcXtfd0Bra0I9e3xI-WTJz1K7I&form_id=jobs_search")
#driver.get("https://europa.eu/europass/en/find-jobs?keyword=physics&location=Germany&order=relevance&form_build_id=form-zOoMCg_qOYhO62ptpWArlEdRosmGYl1w2prOh_JGUSQ&form_id=jobs_search")
time.sleep(2)

cookies = driver.find_element(By.LINK_TEXT,"Accept only essential cookies")
cookies.click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='cookie-consent-banner']/div/div/div[2]/button"))).click()


keywords = ["data science","physics","science","scientist","machine learning","deep learning"]
# scraping logic...

job_cards = driver.find_elements(By.CSS_SELECTOR,".row")

jobs = []
job_details = {}

titles = []
description = []
links = []

N_pages = 5
for page in tqdm(range(N_pages)):
    time.sleep(2)
    scroll_to = driver.find_element(By.ID,"edit-block-title")
    
    job_cards = driver.find_elements(By.CSS_SELECTOR,".row")
    for job in job_cards:
        try:
            title_ele  = job.find_element(By.CSS_SELECTOR,".jobs--title")
            title_text = title_ele.text
            #print(title_text)
            description_ele = job.find_element(By.CSS_SELECTOR,".node-content") #.find_element(By.CSS_SELECTOR,".field-item__description jsDescription collapsed")
            description_text = description_ele.text
            #print(description_ele.text)
            #titles.append(title_text)
            if (any(word.lower() in description_text.lower() for word in keywords)):
                titles.append(title_text.strip())
                job_details["Title"] = title_text.strip()
                description.append(description_text.strip())
                job_details["Description"] = description_text.strip()
                
                link_button = job.find_element(By.CSS_SELECTOR,".boxButtonslist")
                link = link_button.find_elements(By.TAG_NAME,'a')
                links.append(str(link[1].get_attribute("href")).split('?')[0])
                job_details["Link"] = links[-1]
                jobs.append(job_details)
        except:
            print("something wrong")
            pass
    try:
        nextpage_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ecl-pagination__item--next')))
        nextpage_button.click()
    except:
        print("something wrong in next")
        break

    
# close the browser and free up the resources
time.sleep(2)
driver.quit()
