import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse
import sys
import pandas as pd
import re

# https://curlconverter.com/ copy as curl(bash)
cookies = {
    'PLACEGE': '826t94aj92sg17mb0828ikq0g6',
    'plc[lang]': 'Q2FrZQ%3D%3D.NKw%3D',
    '_ga': 'GA1.1.1628457313.1709207010',
    'plc[fb_popup_shown]': 'Q2FrZQ%3D%3D.dw%3D%3D',
    'plc[mode]': 'Q2FrZQ%3D%3D.KrDcFg%3D%3D',
    '_ga_B8GK75F5FJ': 'GS1.1.1709801325.9.0.1709801325.60.0.0',
}

headers = {
    'authority': 'place.ge',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': 'PLACEGE=826t94aj92sg17mb0828ikq0g6; plc[lang]=Q2FrZQ%3D%3D.NKw%3D; _ga=GA1.1.1628457313.1709207010; plc[fb_popup_shown]=Q2FrZQ%3D%3D.dw%3D%3D; plc[mode]=Q2FrZQ%3D%3D.KrDcFg%3D%3D; _ga_B8GK75F5FJ=GS1.1.1709801325.9.0.1709801325.60.0.0',
    'dnt': '1',
    #'referer': 'https://place.ge/ru/ads?object_type=flat&mode=list&nearest=0&type=for_rent&condition=&project=&agency_id=&city_id=1&region_id=&district_id=&street_id=&commercial_type=&commercial_type2=&status=&rooms_from=2&rooms_to=2&living_space_from=40&living_space_to=%D0%B4%D0%BE&price_from=%D0%BE%D1%82&price_to=1500&currency_id=1&with_photos=0&owner=0&owner=1',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

params = {
    'type': 'for_rent',
    'object_type': 'flat',
    'rooms_from': '2',
    'rooms_to': '2',
    'price_to': '1500',
    'currency_id': '1',
    'living_space_from': '40',
    'city_id': '1',
    'owner': '1',
    'mode': 'list',
    'order_by': 'date',
    'limit': '100',
}

class Apartment:
    id = 0
    date = ""
    price = 0
    area = 0
    rooms = 0
    floor = 0
    max_floor = 0
    district = ""
    neighborhood = ""
    address = ""
    tel = ""
    #price per square meter

def main():
    response = requests.get('https://place.ge/ru/ads', params=params, cookies=cookies, headers=headers)
    if response.status_code != 200:
        print (f"Сайт вернул код: {response.status_code}")
        sys. exit()

    soup = BeautifulSoup(response.text, 'html.parser')
    #df = pd.DataFrame(columns=['price', 'area', 'rooms'])

    #left > div.leftSite > div.recommended > div.boxProdFilter > div.tr-line.paid-ad > div.photo-info > div.infoFilter
    table = soup.find('div', {'class': 'boxProdFilter'})
    apartments = []

    for row in table.find_all('div', {'class': 'tr-line'})[1:]:
        info_filter = row.find('div', {'class': 'infoFilter'})
        edit_filter = row.find('div', {'class': 'editFilter'})

        #"ID: 1276813"
        id = search_field(r'ID:\s?(\d+)', edit_filter.text.strip(), 0)
        
        #<em>добавлено: </em>
        date = search_field(r'(\d+.\d+.\d+)', edit_filter.find('span', {'class': 'pub-date'}).text.strip(), "")

        #<strong>5,000 лари / месяц</strong>
        price_thousand = search_field(r'(\d+),\d+ лари / месяц', info_filter.find('span', {'class': 'price'}).text.strip(), 0)
        price_rest = search_field(r'(\d+) лари / месяц', info_filter.find('span', {'class': 'price'}).text.strip(), 0)
        try:
            price = int(price_thousand)*1000 + int(price_rest)
        except:
            print("price = int({price_thousand})*1000 + int({price_rest})")
            price = 0
        
        #, квартира, 4 комнаты, 118 м кв., этаж 3/10
        area = search_field(r'(\d+) м кв.', info_filter.text.strip(), 0)
        rooms = search_field(r'(\d+) комнат', info_filter.text.strip(), 0)
        floor = search_field(r'этаж (\d+)', info_filter.text.strip(), 0)
        max_floor = search_field(r'этаж \d+/(\d+)', info_filter.text.strip(), 0)
        # Тбилиси, Сабуртало, пр. Важа-Пшавела
        district = search_field(r'Тбилиси, (\w+),', info_filter.text.strip(), "")
        address = search_field(r'Тбилиси, \w+, (\w+),', info_filter.text.strip(), "")
        #тел: 5-97-799292, Ia, агент 
        tel = search_field(r'тел: ([0-9-]+)', info_filter.text.strip(), "")

        apartment = Apartment()
        apartment.id = id
        apartment.date = date
        apartment.price = price
        apartment.area = area
        apartment.rooms = rooms
        apartment.floor = floor
        apartment.max_floor = max_floor
        apartment.district = district
        apartment.neighborhood = ""
        apartment.address = address
        apartment.tel = tel

        apartments.append(apartment)

    df = pd.DataFrame([vars(ap) for ap in apartments])
    print(df)

def search_field(regular, text, default_value):
    value = default_value
    result = re.search(regular, text)
    if (result):
        value = result.group(1)

    return value
    
if (__name__ == "__main__"):
    main()