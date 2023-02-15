import requests
from bs4 import BeautifulSoup
from scraping.models import Link


# class Command(BaseCommand):
#     help = 'Scrape'
#
#     def handle(self, *args, **options):
def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


url = 'https://r.onliner.by/ak/?rent_type%5B%5D=1_room&rent_type%5B%5D=2_rooms&rent_type%5B%5D=3_rooms&rent_type%5B%5D=4_rooms&rent_type%5B%5D=5_rooms&rent_type%5B%5D=6_rooms'

print(get_html(url))