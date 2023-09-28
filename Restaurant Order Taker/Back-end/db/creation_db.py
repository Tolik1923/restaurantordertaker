import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    con = psycopg2.connect(dbname="postgres", user="myuser", host="db", password="qwezxc")
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
    cur = con.cursor()
    
    try:
        cur.execute(sql.SQL("CREATE DATABASE restaurant;"))
    except psycopg2.errors.DuplicateDatabase:
        pass
    finally:
        cur.close()
        con.close()
