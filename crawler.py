from pyvirtualdisplay import Display
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
            chromedriver = '/usr/lib/chromium-browser/chromedriver'
            driver_0 = webdriver.Chrome(chromedriver)
            try:
                driver_0.get(add)
                things_0 = driver_0.find_elements_by_css_selector(
                    '#company-list div.company-name a:nth-child(1)')
                #driver_0.implicitly_wait(10)
                comp_names = []
                comp_links = []
                for t in things_0:
                    comp_name = t.text
                    comp_names.append(t.text)
                    link_0 = t.get_attribute("href")
                    comp_link = link_0
                    comp_links.append(link_0)

                    chromedriver = '/usr/lib/chromium-browser/chromedriver'
                    driver_1 = webdriver.Chrome(chromedriver)
                    try:
                        driver_1.get(link_0)
                        things_1 = driver_1.find_elements_by_css_selector(
                            '#company-jobs div.ui.job-title.header a')
                        job_names = []
                        job_links = []
                        for f in things_1:
                            job_name = f.text
                            job_names.append(f.text)
                            link_1 = f.get_attribute("href")
                            job_link = link_1
                            job_links.append(link_1)

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
        chromedriver = '/usr/lib/chromium-browser/chromedriver'
        driver_2 = webdriver.Chrome(chromedriver)

        try:
            driver_2.get(link)

            company_name = comp_name
            title = job_name
            condition = driver_2.find_elements_by_css_selector('div.job-stat-info')
            main = driver_2.find_elements_by_css_selector('#job-duty')
            detail = driver_2.find_elements_by_css_selector('#job-content')

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
                self.jobsdao.save_jobs(link, str(company_name), str(title), str(condition), str(main), str(detail))

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
        finally:
            driver_2.quit()
	


display = Display(visible=0, size=(800, 600))
display.start()

adds = ["https://www.rocketpunch.com/jobs?career_type=1&keywords=머신러닝&keywords=machine%20learning&keywords=data&keywords=python&keywords=machine-learning&keywords=data-analysis&page={}&q=".format(i) for i in range(1,12)]

jobsdao = JobsDAO()

crawler = RocketPunchJobsCrawler(jobsdao, adds)
crawler.crawl_link()

jobsdao.close()

display.stop()
