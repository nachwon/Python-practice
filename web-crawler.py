import requests
from bs4 import BeautifulSoup

url = requests.get('http://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat')
data = url.text
bs = BeautifulSoup(data,'html.parser')
title_list = bs.find_all('td', class_='title')
rating_list = bs.find_all('div', class_='rating_type')
date_list = bs.find_all('td', class_='num')

for i, j, k in zip(title_list, rating_list, date_list):
    print(f'제목: {i.a.text}, 평점: {j.strong.text}, 날짜: {k.text}')