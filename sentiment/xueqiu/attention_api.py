'''
Created on 2017年11月16日

@author: liqing
'''
import time
from datetime import datetime
import requests
import json
from myutils.mysql_util import batch_save_date_to_db


def pasrse_html(html, key_name):
    json_data = json.loads(html)
    json_data = json_data.get("list", [])
    now = datetime.now()
    now = now.date()
    datas = []
    for ele in json_data:
        symbol = ele.get("symbol", "")
        name = ele.get("name", "")
        key_value = ele.get(key_name, 0)
        datas.append([now, symbol, name, key_value])
    
    return datas
    

def get_data(grab_url, key_name, in_sql):
    url = 'https://xueqiu.com/hq'
    
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
    
    
    
    referer = url
    
    datas = []
    for i in range(116):
        headers["Referer"] = referer
        url = grab_url % (i + 1)
        
        print(url)
        r = requests.get(url, headers=headers, cookies=cookies)
    
        da = pasrse_html(r.text, key_name)
        datas.extend(da)
        time.sleep(1)
    
    batch_save_date_to_db(in_sql, datas)

def get_follow_data():
    grab_url = "https://xueqiu.com/stock/screener/screen.json?category=SH&exchange=&areacode=&indcode=&orderby=follow7d&order=desc&current=ALL&pct=ALL&page=%s&follow7d=0_8111&_=1510827697535"
    key_name = "follow7d"
    in_sql = " replace into  follow_xueqiu(f_date,symbol,name,follow,up_time) values(%s,%s,%s,%s,now()) "
    get_data(grab_url, key_name, in_sql)
    

def get_tweet_data():
    grab_url = "https://xueqiu.com/stock/screener/screen.json?category=SH&exchange=&areacode=&indcode=&orderby=tweet7d&order=desc&current=ALL&pct=ALL&page=%s&tweet7d=0_4266&_=1510827621337"
    key_name = "tweet7d"
    in_sql = " replace into  tweet_xueqiu(f_date,symbol,name,tweet,up_time) values(%s,%s,%s,%s,now()) "
    get_data(grab_url, key_name, in_sql)

if __name__ == "__main__":
    get_follow_data()
    get_tweet_data()
    
