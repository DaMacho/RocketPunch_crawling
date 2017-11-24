from pyvirtualdisplay import Display    # to run in aws ec2 env
from selenium import webdriver          # to enter and get info from job posts

import requests                         # to enter search results api pages
import json                             # to read info from api pages
import re                               # to get info from api pages
import datetime
print(datetime.datetime.now())

from jobsdao import JobsDAO
from jobsdao_mongo import save_jobs

'''
Class RocketPunchJobsCrawler take 2 object.
One is MySQL data access object.
Another is list of api page links from search results.

job post addresses are from RocketPunch's api page.
Took it from search result page.

# to explain, (total address is on line 115)
https://www.rocketpunch.com/api/jobs/template?  --api page, jobs search result.
career_type=1&                                  --results including entry-level.
keywords=%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D&  --Korean word, machine-learning.
keywords=machine%20learning&                    --English, machine learning.
keywords=data&
keywords=python&
keywords=machine-learning&
keywords=data-analysis&
page={}&q="                                     --for page number.

## Can edit for own purpose.
'''

class RocketPunchJobsCrawler(object):
    def __init__(self, jobsdao, adds):
        self.jobsdao = jobsdao
        self.adds = adds

    # Get job post addresses from api page
    def get_forms(self, link):
        response = requests.get(link)
        contents = json.loads(response.text)
        info = contents['data']['template']
        form = re.finditer(r'(/jobs/[^t]\d+/\S+[^"\s])', info)
        return form

    # Make full job post links from forms and ready to enter eatch links
    def crawl_link(self):
        for add in self.adds:
            try:
                for form in self.get_forms(add):
                    job_link = ("https://www.rocketpunch.com{}".format(form.group()))
                    try:
                        self.crawl_info(job_link)
                    except Exception:
                        continue

            except Exception as e:
                print(e)
                break

    # Link to job links by selenium and gather information
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

            ## just for monitoring
            print(link)
            print(company_name[0].text)
            print(title[0].text)
            print(datetime.datetime.now())

            company_name = company_name[0].text
            title = title[0].text
            condition = condition[0].text
            main = main[0].text
            detail = detail[0].text[:-4]

            try:
                ## to save info into mongodb
                save_jobs(link, company_name,
                          title, condition, main, detail)

                ## to save info into mysql
                self.jobsdao.save_jobs(link, str(company_name),
                                       str(title), str(condition),
                                       str(main), str(detail))

            except Exception as e:
                print(e)

        except Exception as e:
            print(e)
        finally:
            driver_2.quit()


# Purpose to run on AWS server
display = Display(visible=0, size=(800, 600))
display.start()

# list of search result api page addresses
adds = ["https://www.rocketpunch.com/api/jobs/template?career_type=1&keywords=%EB%A8%B8%EC%8B%A0%EB%9F%AC%EB%8B%9D&keywords=machine%20learning&keywords=data&keywords=python&keywords=machine-learning&keywords=data-analysis&page={}&q=".format(i) for i in range(1,15)]

jobsdao = JobsDAO()

crawler = RocketPunchJobsCrawler(jobsdao, adds)
crawler.crawl_link()

jobsdao.close()

display.stop()
