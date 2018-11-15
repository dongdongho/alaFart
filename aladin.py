from bs4 import BeautifulSoup
import requests
import urllib

base_url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?'
encoding_type = 'EUC-KR'

def search_book(keyword):
    book_list = []
    params = {'SearchTarget':'UsedStore','SortOrder':11}
    params['SearchWord'] = keyword

    url =  base_url + urllib.parse.urlencode(params, encoding = encoding_type)
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content, 'lxml')
    items = soup.find_all(class_='ss_book_box')

    for item in items:
        if item.find(class_='usedshop_off_text3') is None:
            continue
        book_list.append(process_raw_data(item))
    return book_list


def process_raw_data(raw_data):
    book = {}
    book['id'] = raw_data['itemid']
    book['name'] = raw_data.find(class_="bo3").string
    if raw_data.find(class_="i_cover"):
        book['cover_img'] = raw_data.find(class_="i_cover")['src']
        
    data = raw_data.find(class_="ss_book_list").find_next('ul').find_all('li')[1].string
    split_data = data.split('|')
    try:
        book['writer'] = split_data[0].strip() if split_data[0].strip() else ''
        book['publisher'] = split_data[1].strip() if split_data[1].strip() else ''
        book['publishing_day'] = split_data[2].strip() if split_data[2].strip() else ''
    except IndexError:
        print("These is missing data, but it's okay.")

    book['detail_info'] = []
    off_list = raw_data.find_all(class_='usedshop_off_text3')
    for off in off_list:
        book['detail_info'].append({'name' : off.string, 'url' : off['href']})

    return book