import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, urlparse
import sys

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
    'object_type': 'flat',
    'mode': 'list',
    'nearest': '0',
    'type': 'for_rent',
    'condition': '',
    'project': '',
    'agency_id': '',
    'city_id': '1',
    'region_id': '',
    'district_id': '',
    'street_id': '',
    'commercial_type': '',
    'commercial_type2': '',
    'status': '',
    'rooms_from': '2',
    'rooms_to': '2',
    'living_space_from': '40',
    'living_space_to': 'до',
    'price_from': 'от',
    'price_to': '1500',
    'currency_id': '1',
    'with_photos': '0',
    'owner': [
        '0',
        '1',
    ],
}

response = requests.get('https://place.ge/ru/ads', params=params, cookies=cookies, headers=headers)
if response.status_code != 200:
    print (f"Сайт вернул код: {response.status_code}")
    sys. exit()

soup = BeautifulSoup(response.text, 'html.parser')

#left > div.leftSite > div.recommended > div.boxProdFilter > div.tr-line.paid-ad > div.photo-info > div.infoFilter
table = soup.find('div', {'class': 'boxProdFilter'})
infos = []
#print(table)
for row in table.find_all('div', {'class': 'tr-line'})[1:]:
    #print(row)
    info = row.find('div', {'class': 'infoFilter'}).text.strip()
    infos.append(info)

print(infos)