# -*- coding: UTF-8 -*-
# 爬器豆瓣读书栏目的top250
import requests
from bs4 import BeautifulSoup
import sqlite3
import re


def get_top250(link):
    # 报头
    headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/61.0.3163.100 Safari/537.36'}
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.find_all(attrs={"class":"item"}):  
        name = item.find(attrs={"class":"pl2"}).find("a")
        detail = item.find(attrs={"class":"pl"}).get_text()
        star = item.find(attrs={"class":"rating_nums"})
        comment_num = item.find(attrs={"class":"star"}).find(attrs={"class":"pl"})
        dictum = item.find(attrs={"class":"inq"})
        print('****************************************************')
        title = name.get('title')
        book_id = re.sub(r'\D{7,}','',name.get('href')[:-1])
        star = star.get_text()
        comment_num = re.sub("\D","",comment_num.get_text())
        image_url = item.find(attrs={"class":"nbg"}).find("img").get("src")
        print(title)
        print(book_id)
        print(detail)
        print(star)
        print(comment_num)
        if not dictum:
            dictum = '无'
        else:
            dictum = dictum.get_text()
        print(dictum)            
        print(image_url)
        sql = "insert into spride_top250 values(null, '%s','%s','%s','%s','%s','%s','%s')"%(title,detail, star,comment_num, dictum, image_url, book_id)
        c.execute(sql)
        conn.commit()
        

          
if __name__=='__main__':
    link = 'https://book.douban.com/top250?start='
     # 连接sqlite数据库
    conn = sqlite3.connect('../../db.sqlite3')
    c = conn.cursor()
    c.execute("delete from spride_top250")
    c.execute("update sqlite_sequence SET seq = 0 where name ='spride_top250'")
    for i in range(0,10):
        link = 'https://book.douban.com/top250?start='+str(i*25)
        get_top250(link)
    # 关闭数据库连接
    conn.close()