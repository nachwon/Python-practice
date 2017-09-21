import requests
import re
from collections import namedtuple
from bs4 import BeautifulSoup


Episode = namedtuple('Episode', ['Img_url', 'Title', 'Rating', 'Date', 'No'])

def get_webtoon_list(web_id, *args):
    episode_list = []
    
    if args[0] == 'full':
        custom_generator = range(1, 60)
    elif len(args) == 2:
        custom_generator = range(args[0], args[1] + 1)
    elif len(args) == 1:
        custom_generator = range(args[0], args[0] + 1)
    
    else:
        custom_generator = range(1, 2)


    # 루프로 돌면서 html 데이터 모으기
    for page_num in custom_generator:
        payload = {'titleId': web_id, 'page': page_num}
        url = requests.get('http://comic.naver.com/webtoon/list.nhn?', params=payload)
        data = url.text
        bs = BeautifulSoup(data, 'lxml')

        # 글번호 추출
        content_no = bs.find_all('td', class_='title')
        no_list = []
        for i in content_no:
            item = i.a.get('href')
            item_no = re.search(r'&no=(\d.*)&', item)
            no_list.append(item_no.groups()[0])
        # 글제목 추출
        title_list = bs.find_all('td', class_='title')
        # 평점 추출
        rating_list = bs.find_all('div', class_='rating_type')
        # 날짜 추출
        date_list = bs.find_all('td', class_='num')
        # 이미지 주소 추출
        imgs = bs.find_all('tr')
        img_list = []
        for i in imgs:
            try:
                if i.img.get('alt') == 'AD 배너':
                    pass
                else:
                    img_list.append(i.img.get('src'))
            except:
                pass

        # 네임드 튜플로 모으기
        # Episode = namedtuple('Episode', ['Img_url', 'Title', 'Rating', 'Date', 'No'])
        for img, title, rating, date, no in zip(img_list, title_list, rating_list, date_list, no_list):
            episode_list.append(
                Episode(Img_url=img, 
                Title=title.a.text, 
                Rating=rating.strong.text, 
                Date=date.text,
                No=no))

        if episode_list[-1].No == '1':
            break
        else:
            continue
            
    return episode_list

def get_webtoon_info(web_id):
    Info = {}
    info_url = requests.get(f'http://comic.naver.com/webtoon/list.nhn?titleId={web_id}')
    info_data = info_url.text
    info_bs = BeautifulSoup(info_data, 'lxml')

    webtoon_title = info_bs.select_one('h2')
    Info['Webtoon_title'] = webtoon_title.contents[0].strip()
    wrt_name = webtoon_title.find('span', class_='wrt_nm')
    Info['Author'] = wrt_name.text.strip()
    
    return Info

def get_webtoon_id(day):
    day_url = requests.get(f'http://comic.naver.com/webtoon/weekdayList.nhn?week={day}')
    day_data = day_url.text
    day_bs = BeautifulSoup(day_data, 'lxml')

    thumbnail = day_bs.find_all('ul', class_='img_list')
    thumbnail_div = thumbnail[0].find_all('div', class_='thumb')

    webtoon_id_list = []

    id_title = namedtuple('webtoon', ['Id', 'Title'])
    for i in thumbnail_div:
        id_a_href = i.a.get('href')
        webtoon_id = re.search(r'Id=(\d*)[&]', id_a_href)
        webtoon_title = i.a.get('title')
        webtoon_id_list.append(id_title(Id=webtoon_id.group(1), Title=webtoon_title))

    return webtoon_id_list

def webtoon_search(keyword):
    search_url = requests.get(f'http://comic.naver.com/search.nhn?keyword={keyword}')
    search_data = search_url.text
    search_bs = BeautifulSoup(search_data, 'lxml')

    searched_dict = {}
    search_result = search_bs.find_all('ul', class_='resultList')
    search_result_a = search_result[0].a.get('href')

    search_id = re.search(r'Id=(\d*)', search_result_a)
    searched_id = search_id.group(1)
    searched_dict['Id'] = searched_id
    searched_dict['Title'] = search_result[0].a.text
    
    return searched_dict
