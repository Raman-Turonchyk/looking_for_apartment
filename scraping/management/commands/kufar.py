from django.core.management.base import BaseCommand

import requests
from bs4 import BeautifulSoup
import time
from scraping.models import Link
import re


class Command(BaseCommand):
    help = 'Scrape'

    def handle(self, *args, **options):
        def get_html(url):
            r = requests.get(url)
            if r.ok:
                return r.content

        def class_full_name(block, class_name):
            full_name = re.findall(fr'{class_name}.*?(?=")', str(block))
            if full_name:
                return full_name[-1]

        def get_page_data(html):
            soup = BeautifulSoup(html, 'lxml')
            sections = soup.find_all('section')

            count = 1
            ost = len(sections)

            for section in sections:

                try:
                    link = section.find('a').get('href')
                except AttributeError:
                    link = 'link'

                try:
                    room = section.find('div', class_=class_full_name(section, class_name="styles_parameters")).text[0]
                except AttributeError:
                    room = None

                try:
                    all_address = section.find('span',
                                               class_=class_full_name(section, class_name="styles_address")).text.split(',')
                    address = ' '.join(all_address[:2])
                    region = all_address[-1].strip()
                except AttributeError:
                    address = None
                    region = None

                try:
                    section_price = section.find('span',
                                                 class_=class_full_name(section, class_name="styles_price__usd")).text
                    price_list = re.findall(r'(\d\s*\d+\.*\d*)', section_price)
                    if not price_list:
                        price = None
                    else:
                        price_str = ''.join([i for i in price_list[0] if i != ' '])
                        price = int(float(price_str))
                except AttributeError:
                    price = None

                if not Link.objects.filter(address=address, price=price, region=region) or not\
                        Link.objects.filter(link=link):
                    Link.objects.create(
                        link=link,
                        room=room,
                        region=region,
                        address=address,
                        price=price,
                        city_id=1
                    )

                print(f'Выполнено {count} итераций, осталось {ost - count} итераций.')
                time.sleep(0.5)
                count += 1

        for i in range(1, 6):
            url = f'https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/{i}k?cur=USD'

            get_page_data(get_html(url))
            print(f'Работа завершена. Все новые {i} - комнатные квартиры найдены!')
            time.sleep(5)
