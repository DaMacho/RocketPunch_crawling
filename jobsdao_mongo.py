from pymongo import MongoClient
import datetime

def find_jobs(link):
    user = ''
    pwd = ''
    host = ''
    port = 
    mongo = MongoClient('mongodb://%s:%s@%s:%s' % (user,pwd,host,port))

    jobs = mongo.mydata.jobs
    found = jobs.find_one({'_id' : link})

    mongo.close()

    return found != None

#    if found:
#        return True
#    return False

def save_jobs(job_link, company_name,
              title, condition, main,
              detail):
    user = ''
    pwd = ''
    host = ''
    port = 
    mongo = MongoClient('mongodb://%s:%s@%s:%s' % (user,pwd,host,port))

    jobs = mongo.mydata.jobs

    if not find_jobs(job_link):
        document = {}
        document['_id'] = job_link
        document['company_name'] = company_name
        document['title'] = title
        document['condition'] = condition
        document['main'] = main
        document['detail'] = detail
        document['datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        jobs.insert_one(document)

    mongo.close()
