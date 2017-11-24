import config as cfg
import pymysql
import datetime

'''
Class JobsDAO is to access to MySQL and process information.
Make connection to MySQL server through configuration information.
'''

class JobsDAO(object):
    def __init__(self):
        self.db = pymysql.connect(host=cfg.DB_HOST, port=cfg.DB_PORT,
                                  user=cfg.DB_USER, passwd=cfg.DB_PWD,
                                  db=cfg.DB_DB, charset='utf8')

    def save_jobs(self, jobs_id, company_name,
                  title, condition,
                  main, detail):
        if not self.get_jobs_by_id(jobs_id):
            title = title.replace("'", '').replace('"', '')
            condition = condition.replace("'", '').replace('"', '')
            main = main.replace("'", '').replace('"', '')
            detail = detail.replace("'", '').replace('"', '')

            query = """INSERT INTO jobs VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')""" \
                    .format(jobs_id, company_name, title,
                            condition, main, detail,
                            datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))

            cursor = self.db.cursor()
            try:
                cursor.execute(query)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                print(e)
            finally:
                cursor.close()

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
