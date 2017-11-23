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
            driver_0 = webdriver.Chrome(chromedriver)
            try:
                driver_0.get(add)
                things = driver_0.find_elements_by_css_selector(
                    '#company-list div.company-name a:nth-child(1)')
                #driver_0.implicitly_wait(10)
                comp_names = []
                comp_links = []
                for t in things:
                    comp_name = t.text
                    comp_names.append(t.text)
                    link = t.get_attribute("href")
                    comp_link = link
                    comp_links.append(link)

                    chromedriver = 'D:/DSS/chromedriver_win32/chromedriver.exe'
                    driver_1 = webdriver.Chrome(chromedriver)
                    try:
                        driver_1.get(link)
                        things = driver_1.find_elements_by_css_selector(
                            '#company-jobs div.ui.job-title.header a')
                        job_names = []
                        job_links = []
                        for t in things:
                            job_name = t.text
                            job_names.append(t.text)
                            link = t.get_attribute("href")
                            job_link = link
                            job_links.append(link)

                            try:
                                self.crawl_info(job_link, comp_name, job_name)
                            except Exception:
                                continue

                    except Exception as e:
                        print(e)
                    finally:
                        driver_1.quit()

            except Exception as e:
                print(e)
            finally:
                driver_0.quit()

    def crawl_info(self, link, comp_name, job_name):
        chromedriver = 'D:/DSS/chromedriver_win32/chromedriver.exe'
        driver_2 = webdriver.Chrome(chromedriver)

        try:
            driver_2.get(link)

            company_name = comp_name
            title = job_name
            condition = driver.find_elements_by_css_selector('div.job-stat-info')
            main = driver.find_elements_by_css_selector('#job-duty')
            detail = driver.find_elements_by_css_selector('#job-content')

            print(company_name)
            print(link)
            print(title)
            # print(condition[0].text)
            # print()
            # print(main[0].text)
            # print()
            # print(detail[0].text[:-4])
            # print(datetime.datetime.now())
            condition = condition[0].text
            main = main[0].text
            detail = detail[0].text[:-4]

            try:
                save_jobs(link, company_name,
                          title, condition, main, detail)
                self.jobsdao.save_jobs()

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
        finally:
            driver_2.quit()


adds = ["https://www.rocketpunch.com/jobs?career_type=1&keywords=머신러닝&keywords=machine%20learning&keywords=data&keywords=python&keywords=machine-learning&keywords=data-analysis&page={}&q=".format(i) for i in range(1,12)]
jobsdao = JobsDAO()
crawler = RocketPunchJobsCrawler(jobsdao, adds)
crawler.crawl_link()

jobsdao.close()
