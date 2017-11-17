'''
Created on 2017年11月17日

@author: liqing
'''

import os
import sys
import requests
import json
import traceback
from datetime import datetime

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from myutils.mysql_util import batch_save_date_to_db



def get_data():
    url = 'http://www.iwencai.com'
    headers = {
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }
    
    r = requests.get(url, headers=headers)
    cookies = r.cookies
    
    for key, value in cookies.items():
        print(key, value)
    print(r.headers)
    
    headers["Cache-Control"] = "no-cache"
    headers["Pragma"] = "no-cache"
    referer = url
    headers["Referer"] = referer
    url = "http://www.iwencai.com/data-robot/extract-new?query=%E5%85%B3%E6%B3%A8%E5%BA%A6&firstDraw=1"
    r = requests.get(url, headers=headers, cookies=cookies)
    
    datas = []
    now = datetime.now()
    now = now.date()
    headers["Referer"] = "http://www.iwencai.com/stockpick/robot-search?w=%E5%85%B3%E6%B3%A8%E5%BA%A6&querytype=stock&robotResultPerpage=30"
    for i in range(50):
        url = "http://www.iwencai.com/stockpick/cache?token=83c3d207f99fa1fccbffdbeb5cfa6200&p=" + str(i + 1) + "&perpage=70&showType=[%22%22,%22%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22,%22onTable%22]"
        print(url)
        r = requests.get(url, headers=headers, cookies=cookies)
        json_data = json.loads(r.text)
        result = json_data.get("result",[])
        for ele in result:
            symbol = ele[0]
            name = ele[1]
            follow_iwencai = ele[4]
            try:
                if follow_iwencai != "--":
                    follow_iwencai = float(follow_iwencai)
                else:
                    follow_iwencai = 0
            except:
                print(traceback.format_exc())
                follow_iwencai = 0
            follow_xueqiu = ele[5]
            try:
                if follow_xueqiu != "--":
                    follow_xueqiu = float(follow_xueqiu)
                else:
                    follow_xueqiu = 0   
            except:
                print(traceback.format_exc())
                follow_xueqiu = 0
            follow_hexun = ele[6]
            try:
                if follow_hexun != "--":
                    follow_hexun = float(follow_hexun)
                else:
                    follow_hexun = 0   
            except:
                print(traceback.format_exc())
                follow_hexun = 0
                
            da = [now,symbol,name,follow_iwencai,follow_xueqiu,follow_hexun]
            datas.append(da)
    
    in_sql = "replace into  follow_iwencai(f_date,symbol,name,follow_iwencai,follow_xueqiu,follow_hexun,up_time) values(%s,%s,%s,%s,%s,%s,now()) "
    
#     for da in datas:
#         print(da)
    
    batch_save_date_to_db(in_sql,datas)
    
    
    
    
    
    

if __name__ == '__main__':
    get_data()
