from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from django.core.management.base import BaseCommand
from scraping.models import Link
import re


class Command(BaseCommand):
    help = 'Scrape'

    def handle(self, *args, **options):
        def string_converter(text):
            return ' '.join(text.split())

        urls = {
            '1': 'https://r.onliner.by/ak/?rent_type%5B%5D=1_room#bounds%5Blb%5D%5Blat%5D=53.75015083799405&bounds%5Blb%5D%5Blong%5D=27.34249307208699&bounds%5Brt%5D%5Blat%5D=54.04600901977141&bounds%5Brt%5D%5Blong%5D=27.781846402791043',
            '2': 'https://r.onliner.by/ak/?rent_type%5B%5D=2_rooms#bounds%5Blb%5D%5Blat%5D=53.75015083799405&bounds%5Blb%5D%5Blong%5D=27.34249307208699&bounds%5Brt%5D%5Blat%5D=54.04600901977141&bounds%5Brt%5D%5Blong%5D=27.781846402791043',
            '3': 'https://r.onliner.by/ak/?rent_type%5B%5D=3_rooms#bounds%5Blb%5D%5Blat%5D=53.75015083799405&bounds%5Blb%5D%5Blong%5D=27.34249307208699&bounds%5Brt%5D%5Blat%5D=54.04600901977141&bounds%5Brt%5D%5Blong%5D=27.781846402791043',
            '4': 'https://r.onliner.by/ak/?rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms#bounds%5Blb%5D%5Blat%5D=53.75015083799405&bounds%5Blb%5D%5Blong%5D=27.34249307208699&bounds%5Brt%5D%5Blat%5D=54.04600901977141&bounds%5Brt%5D%5Blong%5D=27.781846402791043'}

        options_chrome = webdriver.ChromeOptions()
        options_chrome.add_argument('--headless')

        for room, url in urls.items():

            with webdriver.Chrome(options=options_chrome) as browser:
                browser.get(url)

                WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'classifieds-list')))

                apartments = browser.find_element(By.CLASS_NAME, 'classifieds-list').find_elements(By.TAG_NAME, 'a')
                for apartment in apartments:
                    link = apartment.get_attribute('href')

                    section_room = apartment.find_element(By.CLASS_NAME, 'classified__caption-item_type').text
                    room = string_converter(section_room)[0]

                    section_address = apartment.find_element(By.CLASS_NAME, 'classified__caption-item_adress').text
                    address = string_converter(section_address)

                    region = 'Минск'

                    section_price = apartment.find_element(By.CLASS_NAME, 'classified__price-value').text
                    price = re.findall(r'(\d\s*\d+\.*\d*)', section_price)[0]

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

                print(f'Все новые {room} комнатные квартиры найдены!')