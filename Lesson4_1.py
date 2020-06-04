
from lxml import html
from pprint import pprint
import requests
import re
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
main_link = 'https://yandex.ru/news'
response = requests.get(main_link, headers = header)
dom = html.fromstring(response.text)
blocks = dom.xpath("//td[@class='stories-set__item']")

reviews = []

for block in blocks:
    data = {}
    data['name'] = block.xpath(".//h2[@class='story__title']//a/text()")

    data['source'] = block.xpath(".//div[@class='story__date']/text()")

    for i, k in data.items():
        if i == 'source':
            regex = re.compile('.\d{2}:\d{2}')
            data['source'] = regex.sub('', k[0])

    data['date'] = block.xpath(".//div[@class='story__date']/text()")

    for i, k in data.items():
        if i == 'date':
            data['date'] = re.findall('\d{2}:\d{2}', k[0])

    data['href'] = block.xpath(".//h2[@class='story__title']//a/@href")

    for i, k in data.items():
        if i == 'href':
            data['href'] = 'https://yandex.ru' + k[0]

    reviews.append(data)

client = MongoClient('localhost',27017)
db = client['yandex']
parsing_ya = db.parsing_ya
parsing_ya.delete_many({})
parsing_ya.insert_many(reviews)

for i in parsing_ya.find({}, {'_id':0}):
    print(i)
