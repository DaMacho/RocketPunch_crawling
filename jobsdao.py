import config as cfg
import pymysql
import datetime

class JobsDAO(object):
    def __init__(self):
        self.db = pymysql.connect(host=cfg.DB_HOST, port=cfg.DB_PORT,
                                  user=cfg.DB_USER, passwd=cfg.DB_PWD,
                                  db=cfg.DB_DB, charset='utf8')

    def save_jobs(self, jobs_id,
                  title, condition,
                  main, detail):
        if not self.get_jobs_by_id(jobs_id):
            pass


    def get_jobs_by_id(self, jobs_id):
        query = "SELECT * FROM jobs WHERE ID = '{}'".format(jobs_id)

        try:
            cursor = self.db.cursor()
            cursor.execute(query)

            row = cursor.fetchone()
            return row != None
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(e)
