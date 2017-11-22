from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import datetime
print(datetime.datetime.now())

from jobsdao import JobsDAO
from jobsdao_mongo import save_jobs


# first part
chromedriver = 'D:/DSS/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

try:
    driver.get(adds[0])

    things = driver.find_elements_by_css_selector(
        '#company-list div.company-name a:nth-child(1)')
    #driver.implicitly_wait(10)
    comp_names = []
    comp_links = []
    for t in things:
        print(t.text)
        comp_names.append(t.text)
        link = t.get_attribute("href")
        comp_links.append(link)
        print(link)

    #print(comp_names)
    #print(comp_links)

except Exception as e:
    print(e)

finally:
    driver.quit()


# second part
chromedriver = 'D:/DSS/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

try:
    driver.get(comp_links[0])

    things = driver.find_elements_by_css_selector(
        '#company-jobs div.ui.job-title.header a')
    job_names = []
    job_links = []
    for t in things:
        print(t.text)
        job_names.append(t.text)
        link = t.get_attribute("href")
        job_links.append(link)
        print(link)

    #print(job_names)
    #print(job_links)

except Exception as e:
    print(e)

finally:
    driver.quit()


# third part
chromedriver = 'D:/DSS/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

try:
    driver.get(job_links[0])

    company_name = comp_names[0]
    title = job_names[0]
    condition = driver.find_elements_by_css_selector('div.job-stat-info')
    main = driver.find_elements_by_css_selector('#job-duty')
    detail = driver.find_elements_by_css_selector('#job-content')

    print(company_name)
    print(job_links[0])
    print(title)
    print(condition[0].text)
    print()
    print(main[0].text)
    print()
    print(detail[0].text[:-4])
    print(datetime.datetime.now())

except Exception as e:
    print(e)

finally:
    driver.quit()
