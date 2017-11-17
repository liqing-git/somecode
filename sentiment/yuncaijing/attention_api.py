'''
Created on 2017年11月16日

@author: liqing
'''
import os
import sys
import time
import requests
import traceback
from datetime import datetime
from bs4 import BeautifulSoup
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


from myutils.mysql_util import batch_save_date_to_db

    

def pasrse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("table", class_="table table-ycj table-hover")
    soup = soup.find("tbody")
    soup = soup.find_all("tr")
    now = datetime.now()
    now = now.date()
    
    datas = []
    for tr in soup:
        try:
            tds = tr.find_all("td")
            da = [now]
            name = tds[0].text.strip()
            name = name.split("（")
            symbol = name[1].replace("）", "")
            da.append(symbol.strip())
            name = name[0]
            da.append(name.strip())
            try:
                attention = float(tds[1].text.strip())
            except:
                attention = 0
            da.append(attention)
            try:
                mai = float(tds[2].text.strip())
            except:
                mai = 0
            da.append(mai)
    
            
            try:
                mai_change = tds[3].text.strip().replace("%", "")
                mai_change = float(mai_change.strip()) / 100
            except:
                mai_change = 0
            
            da.append(mai_change)
            datas.append(da)
        except:
            print(traceback.format_exc())
            continue
    
    return datas


def get_data():
    
    url = 'http://www.yuncaijing.com/data/mai/main.html'
    
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
#     for key, value in cookies.items():
#         print(key, value)
#     print(r.headers)
    
    
    datas = []
    
    
    da = pasrse_html(r.text)
    datas.extend(da)
    
    headers["Cache-Control"] = "no-cache"
    headers["Pragma"] = "no-cache"
    referer = url
    for i in range(174):
        headers["Referer"] = referer
        url = "http://www.yuncaijing.com/data/mai/p%s.html" % (i + 2)
        print(url)
        r = requests.get(url, headers=headers, cookies=cookies)
        da = pasrse_html(r.text)
        datas.extend(da)
        referer = url
        time.sleep(1)
        
        
    in_sql = " replace into  attention_yuncaijing(a_date,symbol,name,attention,mai,mai_change,up_time) values(%s,%s,%s,%s,%s,%s,now()) "
    batch_save_date_to_db(in_sql, datas)
    
    
    
    
if __name__ == "__main__":
    get_data()
