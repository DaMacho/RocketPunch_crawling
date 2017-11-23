from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import requests
from bs4 import BeautifulSoup
import json
import re
import time
import datetime
print(datetime.datetime.now())

from jobsdao import JobsDAO
from jobsdao_mongo import save_jobs


class RocketPunchJobsCrawler(object):
    def __init__(self, jobsdao, adds):
        self.jobsdao = jobsdao
        self.adds = adds

    def get_forms(url):
        response = requests.get(url)
        content = response.text
        contents = json.loads(content)
        info = contents['data']['template']
        form = re.finditer(r'(/jobs/[^t]\d+/\S+[^"\s])', info)
        return form

    def crawl_link(self):
        for add in self.adds:
            try:
                for form in get_forms(add):
                    job_link = ("https://www.rocketpunch.com{}".format(form.group()))
                    try:
                        self.crawl_info(job_link)
                    except Exception:
                        continue

            except Exception as e:
                print(e)
                break

    def crawl_info(self, link):
        chromedriver = '/usr/lib/chromium-browser/chromedriver'
        driver_2 = webdriver.Chrome(chromedriver)

        try:
            driver_2.get(link)

            company_name = driver_2.find_elements_by_css_selector('div.company-name')
            title = driver_2.find_elements_by_css_selector('h2.nowrap.job-title')
            condition = driver_2.find_elements_by_css_selector('div.job-stat-info')
            main = driver_2.find_elements_by_css_selector('#job-duty')
            detail = driver_2.find_elements_by_css_selector('#job-content')

            print(link)
            print(company_name[0].text)
            print(title[0].text)
            # print(condition[0].text)
            # print()
            # print(main[0].text)
            # print()
            # print(detail[0].text[:-4])
            # print(datetime.datetime.now())
            company_name = company_name[0].text
            title = title[0].text
            condition = condition[0].text
            main = main[0].text
            detail = detail[0].text[:-4]

            try:
                save_jobs(link, company_name,
                          title, condition, main, detail)
                self.jobsdao.save_jobs(link, str(company_name),
                                       str(title), str(condition),
                                       str(main), str(detail))

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
        finally:
            driver_2.quit()



display = Display(visible=0, size=(800, 600))
display.start()

adds = ["https://www.rocketpunch.com/api/jobs/template?career_type=1&keywords=%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D&keywords=machine%20learning&keywords=data&keywords=python&keywords=machine-learning&keywords=data-analysis&page={}&q=".format(i) for i in range(1,15)]

jobsdao = JobsDAO()

crawler = RocketPunchJobsCrawler(jobsdao, adds)
crawler.crawl_link()

jobsdao.close()

display.stop()
