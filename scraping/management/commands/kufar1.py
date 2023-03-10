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
                return r.text
            print(r.status_code)

        def get_page_data(html, page):
            soup = BeautifulSoup(html, 'lxml')
            sections = soup.find('div', class_='styles_wrapper__tQR7Y').find_all('section')

            count = 1
            ost = len(sections)
            for section in sections:

                try:
                    link = section.find('a', class_='styles_wrapper__l0BVB').get('href')
                except AttributeError:
                    link = ''

                try:
                    room = section.find('div', class_='styles_parameters__f57M3 styles_ellipsis__P3Kz7').text[0]
                except AttributeError:
                    room = None

                try:
                    region = section.find('div', class_='styles_wrapper__Lep7m').find('span').text
                except AttributeError:
                    region = ''

                try:
                    address = section.find('span', class_='styles_address__IYPCx').text
                except AttributeError:
                    address = ''

                try:
                    price = section.find('div', class_='styles_price__BsITs styles_ellipsis__P3Kz7').find_all('span')[
                        1].text
                    price = re.sub(r'(\d*)[ ](\.*\d+)', r'\1\2', price)
                    if price:
                        price = price[0]
                    else:
                        price = None
                except AttributeError:
                    price = None

                if not Link.objects.filter(address=address, price=price, region=region):
                    Link.objects.create(
                        link=link,
                        room=room,
                        region=region,
                        address=address,
                        price=price,
                        city_id=1
                    )

                time.sleep(2)

                print(f'?????????????????? {count} ????????????????, ???????????????? {ost - count} ????????????????, ???????????????? ?????????? ??? {page}')
                count += 1

        for i in range(1, 6):
            url = f'https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/{i}k/bez-posrednikov?cur=USD'
            iteration = 1

            get_page_data(get_html(url), iteration)

            while True:
                get_page_data(get_html(url), iteration)

                soup = BeautifulSoup(get_html(url), 'lxml')

                try:
                    url_link = soup.find('div', class_='styles_links__inner__huze7').find_all('a')
                    url = 'https://re.kufar.by' + url_link[-1].get('href')
                except AttributeError:
                    break

                if len(url_link) < 5 and iteration != 1:
                    print('???????????? ??????????????????')
                    break
                time.sleep(12)
                iteration += 1
