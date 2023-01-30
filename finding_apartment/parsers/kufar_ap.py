import requests
from bs4 import BeautifulSoup
import time
from finding_apartment.models import Link


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    print(r.status_code)


def res(text):
    return text.replace(' $ *', '')


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    sections = soup.find('div', class_='styles_wrapper__tQR7Y').find_all('section')

    count = 1
    ost = len(sections)
    for section in sections:

        try:
            link = section.find('a', class_='styles_wrapper__8rw3D').get('href')
        except AttributeError:
            link = '---'

        try:
            room = section.find('div', class_='styles_parameters__sDPAy styles_ellipsis__Nb6YJ').text[0]
        except AttributeError:
            room = '---'

        try:
            region = section.find('div', class_='styles_wrapper__hYktI').find('span').text
        except AttributeError:
            region = '---'

        try:
            address = section.find('div', class_='styles_wrapper__DyCkx').find_all('span')[1].text
        except AttributeError:
            address = '---'

        try:
            price = res(section.find('div', class_='styles_price__MdLH6 styles_ellipsis__Nb6YJ').find_all('span')[1].text)
        except AttributeError:
            price = '---'

        Link(
                link=link,
                room=room,
                region=region,
                address=address,
                price=price,
                city=1
        ).save()

        time.sleep(1)

        print(f'Выполнено {count} итераций, осталось {ost - count} итераций')
        count += 1


def main():
    url = 'https://re.kufar.by/l/minsk/snyat/kvartiru-dolgosrochno/1k/bez-posrednikov?cur=USD'
    iteration = 1

    get_page_data(get_html(url))

    while True:
        get_page_data(get_html(url))

        soup = BeautifulSoup(get_html(url), 'lxml')

        try:
            url_link = soup.find('div', class_='styles_links__inner__huze7').find_all('a')
            url = 'https://auto.kufar.by' + url_link[-1].get('href')
        except AttributeError:
            break

        if len(url_link) < 5 and iteration != 1:
            break
        time.sleep(10)
        iteration += 1



if __name__ == '__main__':
    main()