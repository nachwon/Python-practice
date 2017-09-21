from WebtoonCrawler import NaverWebtoonCrawler
from utils import *

print('==================================')
print('=      Naver_Webtoon_Crawler     =')
print('==================================')
while True:
    print('type "list" for webtoon id lists')
    print('type "search" to search webtoon id online')
    webtoon_id = input('input webtoon id >>> ')
    print("")

    if webtoon_id == 'list':
        print('type only 3 letters')
        print('Ex: monday: mon')
        day = input('which day? >>> ')
        print("")
        webtoon_list = get_webtoon_id(day)
        for i in webtoon_list:
            print(f'웹툰 번호: {i.Id}, 웹툰 제목: {i.Title}')
        print("")
        continue

    elif webtoon_id == 'search':
        search_keyword = input('search >>> ')
        result_dict = webtoon_search(search_keyword)
        print(f"ID : {result_dict['Id']} Title : {result_dict['Title']}")
        print('')
        continue

    elif webtoon_id == 'q':
        break
        

    try:
        webtoon_id = int(webtoon_id)
        collected_webtoon = NaverWebtoonCrawler(webtoon_id)
        info_dic = get_webtoon_info(webtoon_id)
        print(f'제목: {info_dic["Webtoon_title"]}   작가: {info_dic["Author"]}')
        break
    except ValueError:
        print('type only 6 digit numbers', '\n')
    
    

while True:
    print('')
    print('=============functions============')
    print('1. get episodes')
    print('2. number of total episodes')
    print('3. show list')
    print('4. check update')
    print('5. update list')
    print('6. clear page list')
    print('7. save list')
    print('8. load list')
    print('q. exit')
    print('')
    selection = input('>>> ')
    print('')

    if selection == '1':
        collected_webtoon.clear_episode_list()
        print('if 1 number is given: gets that page')
        print('if 2 numbers are given: gets pages from i to j')
        print("type 'full' to get all the pages", '\n')
        page_num = input('>>> ')
        print('')
        page_num = page_num.split(',')

        if page_num[0] == 'full':
            collected_webtoon.get_episode_list('full')
            print('all pages have been collected')
        elif len(page_num) == 1:
            collected_webtoon.get_episode_list(int(page_num[0]))
            print(f'{webtoon_id}, page {page_num[0]} collected!')
        elif len(page_num) == 2:
            collected_webtoon.get_episode_list(int(page_num[0]), int(page_num[1]))
            print(f'{webtoon_id}, pages from {page_num[0]} to {page_num[1]} collected!')
        continue

    elif selection == '2':
        print(f'there are total {collected_webtoon.total_episode_count()} episodes in this webtoon')

    elif selection == '3':
        if len(collected_webtoon.episode_list) == 0:
            print('episode list is empty')
        for i in collected_webtoon.episode_list:
            print(f'{i.No}. {i.Title}')
        continue

    elif selection == '4':
        collected_webtoon.up_to_date

    elif selection == '5':
        force_update_question = input('force update? [y/n] ')
        print('')
        if force_update_question == 'y':
            collected_webtoon.update_episode_list(force_update=True)
        else:
            collected_webtoon.update_episode_list(force_update=False)

    elif selection == '6':
        print(collected_webtoon.clear_episode_list())

    elif selection == '7':
        savename = input('filename? >>> ')
        print('')
        collected_webtoon.save(savename)

    elif selection == '8':
        loadname = input('filename? >>> ')
        print('')
        collected_webtoon.load(loadname)

    elif selection == 'q':
        break
    else:
        print('wrong input')