# -*- coding: UTF-8 -*-
# 爬器豆瓣读书首页新书速递模块的数据
import requests
from bs4 import BeautifulSoup
import sqlite3
import re


# 抓取的url地址
link = "https://book.douban.com/"
# 报头
headers = {'User_Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/61.0.3163.100 Safari/537.36'}
r = requests.get(link, headers=headers)
# 使用BeautifulSoup解析这段代码
soup = BeautifulSoup(r.text, 'lxml')
names = soup.select("#content > div > div.article > div.section.books-express\
                    > div.bd > div > div > ul > li > div.info > div.title > a")
authors = soup.select("#content > div > div.article > div.section.books-express\
                    > div.bd > div > div > ul > li > div.info > div.author")
images_urls = soup.select('#content > div > div.article > div.section.books-express\
                    > div.bd > div > div > ul > li > div.cover > a > img')
details = soup.select('#content > div > div.article > div.section.books-express\
                    > div.bd > div > div > ul > li > div.info > div.more-meta')
# 连接sqlite数据库
conn = sqlite3.connect('../../db.sqlite3')
c = conn.cursor()
c.execute("delete from spride_latest")
c.execute("update sqlite_sequence SET seq = 0 where name ='spride_latest'")
for item,item2,item3,item4 in zip(names, authors, images_urls, details):
    print(item.get_text())
    print(item2.get_text())
    print(item3.get('src'))
    name = item.get_text()
    author = item2.get_text()
    image_url = item3.get('src')
    detail = item4
    book_id = re.sub(r'\D{7,}','',item.get('href'))
    print('********************************************************************************')
    sql = "insert into spride_latest values(null, '%s','%s','%s', '%s','%s')"%(book_id,name, author, detail, image_url )
    c.execute(sql)
conn.commit()
conn.close()

