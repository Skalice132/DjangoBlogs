import requests
from bs4 import BeautifulSoup as BS

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
           'Accept': 'application/json, text/plain, */*'}

url = 'https://samara.hh.ru/search/vacancy?area=78&fromSearchLine=true&st=searchVacancy&text=Python'
response = requests.get(url, headers=headers)
jobs = []
if response.status_code == 200:
    soup = BS(response.content, 'html.parser')
    main_div = soup.find_all('div', class_="vacancy-serp-item")
    for item in main_div:
        jobs.append({'title': item.find('a', class_='bloko-link HH-LinkModifier').get_text(),
                     'href': item.find('a', class_='bloko-link HH-LinkModifier').get('href').replace('?query=Python',''),
                     'company': item.find('a', class_='bloko-link bloko-link_secondary').get_text().replace(', с опытом работы',''),
                     'content': item.find('div', class_='g-user-content').get_text(),
                     })
