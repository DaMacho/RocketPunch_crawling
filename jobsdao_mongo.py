from pymongo import MongoClient

def find_jobs(link):
    host = ''
    port =
    mongo = MongoClient(host, port)

    jobs = mongo.mydata.jobs
    found = jobs.find_one({'_id' : link})

    mongo.close()

    return found != None

#    if found:
#        return True
#    return False

def save_jobs(job_link, company_name,
              title, condition, main,
              detail, timenow):
    host = ''
    port =
    mongo = MongoClient(host, port)

    jobs = mongo.mydata.jobs

    if not find_jobs(job_link):
        decument = {}
        document['_id'] = job_link
        document['company_name'] = company_name
        document['title'] = title
        document['condition'] = condition
        document['main'] = main
        document['detail'] = detail
        document['datetime'] = timenow

        jobs.insert_one(document)

    mongo.close()