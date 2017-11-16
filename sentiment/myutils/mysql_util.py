'''
Created on 2017年11月16日

@author: liqing
'''
import pymysql
import traceback

def get_db_connect():
    conn = pymysql.connect(host='192.168.123.137', port=3306, user='root', passwd='Kavout@2017', db='sentiment', charset='UTF8')
    return conn

def close_db_connect(conn):
    try:
        if conn:
            conn.close()
    except:
        print(traceback.format_exc())
    finally:
        pass

def batch_save_date_to_db(in_sql,datas):
    
    conn = get_db_connect()
    try:
        cursor = conn.cursor()
        cursor.executemany(in_sql, datas)
        conn.commit()
        cursor.close()
    finally:
        close_db_connect(conn)