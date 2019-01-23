import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sssg.settings')

import django
django.setup()

import sys
import requests
from bs4 import BeautifulSoup
from django.core.files import File 
from shop.models import Item


def trim(s):
    return ' '.join(s.split())


def main(query, pagingIndex):
    url = 'https://search.shopping.naver.com/search/all.nhn?'
    for page in range(1, int(pagingIndex)+1):
        params = {'query': query, 'pagingIndex': page}
        res = requests.get(url, params=params)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        for item_tag in soup.select('#_search_list ._itemSection'):
            name = trim(item_tag.select('a.tit')[0].text)
            price = trim(item_tag.select('.price .num')[0].text).replace(',', '')
            img_url = item_tag.select('img[data-original]')[0]['data-original']
            
            res = requests.get(img_url, stream=True)
            img_name = os.path.basename(img_url.split('?', 1)[0])

            item = Item(name=name, amount=price, is_public=True)
            item.photo.save(img_name, File(res.raw))
            item.save()

if __name__ == '__main__':
    try:
        query = sys.argv[1]
        pagingIndex = sys.argv[2]
        main(query, pagingIndex)
    except IndexError:
        print(f'usage> {sys.argv[0]} <query>')







