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


class RocketPunchJobsCrawler(object):
    def __init__(self, jobsdao, adds):
        self.jobsdao = jobsdao
        self.adds = adds

    def crawl_link(self):
        for add in self.adds:
            chromedriver = 'D:/DSS/chromedriver_win32/chromedriver.exe'
            driver = webdriver.Chrome(chromedriver)

            try:
                driver.get(add)
                things = driver.find_elements_by_css_selector(
                    '#company-list div.company-name a:nth-child(1)')
                #driver.implicitly_wait(10)
                comp_names = []
                comp_links = []
                for t in things:
                    # print(t.text)
                    comp_names.append(t.text)
                    link = t.get_attribute("href")
                    comp_links.append(link)
                    # print(link)
                #print(comp_names)
                #print(comp_links)
            except Exception as e:
                print(e)
            finally:
                driver.quit()


adds = ["https://www.rocketpunch.com/jobs?career_type=1&keywords=머신러닝&keywords=machine%20learning&keywords=data&keywords=python&keywords=machine-learning&keywords=data-analysis&page={}&q=".format(i) for i in range(1,20)]
