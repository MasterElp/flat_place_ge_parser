import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse
import sys
import pandas as pd

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
    infos = []
    apartments = []

    for row in table.find_all('div', {'class': 'tr-line'})[1:]:

        info = row.find('div', {'class': 'infoFilter'})
        infos.append(info.text.strip())

        price = info.find('span', {'class': 'price'}).text.strip()
        #print(price)
        apartment = Apartment()
        apartment.price = 0
        apartment.area = 0
        apartment.rooms = 0
        apartment.floor = 0
        apartment.max_floor = 0
        apartment.district = price
        apartment.neighborhood = ""
        apartment.address = ""
        apartment.tel = ""

        apartments.append(apartment)

    df = pd.DataFrame([vars(ap) for ap in apartments])
    print(df)

if (__name__ == "__main__"):
    main()