# -*- coding: utf-8 -*-
# Configuration file for Data Access Object(DAO) of mysql

# for MySQL
'''
create table jobs (
	ID varchar(500) NOT NULL,
    Company_name varchar(100) NOT NULL,
    Title varchar(100) NOT NULL,
    Condi varchar(100) NOT NULL,
    Main text NOT NULL,
    Detail text NOT NULL,
    CrawlTime datetime NOT NULL,

    PRIMARY KEY (ID)
) DEFAULT CHARSET=utf8;
'''

DB_USER = ''
DB_PWD = ''
DB_HOST = ''
DB_PORT =
DB_DB = ''
