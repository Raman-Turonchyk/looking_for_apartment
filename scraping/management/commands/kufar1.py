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

                print(f'Выполнено {count} итераций, осталось {ost - count} итераций, страница номер № {page}')
                count += 1


        # url = 'https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/1k/bez-posrednikov?cur=USD'
        url = 'https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/1k/bez-posrednikov?cur=USD&gbx=b%3A27.212593274414044%2C53.610880226147074%2C28.106605725585936%2C54.16012964182954&gtsy=country-belarus~province-minsk~locality-minsk&size=30'
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
                print('Работа завершена')
                break
            time.sleep(12)
            iteration += 1
