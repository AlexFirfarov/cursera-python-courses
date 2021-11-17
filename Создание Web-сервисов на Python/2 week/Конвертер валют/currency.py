from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', params={'date_req': date})
    soup = BeautifulSoup(response.content, 'lxml')

    valute_from = soup.find('charcode', text=cur_from)
    value_from = Decimal(valute_from.find_next_sibling('value').string.replace(',', '.'))
    nominal_from = Decimal(valute_from.find_next_sibling('nominal').string)

    valute_to = soup.find('charcode', text=cur_to)
    value_to = Decimal(valute_to.find_next_sibling('value').string.replace(',', '.'))
    nominal_to = Decimal(valute_to.find_next_sibling('nominal').string)

    from_cur_to_rub = amount * value_from / nominal_from
    result = from_cur_to_rub * nominal_to / value_to

    return result.quantize(Decimal('.0001'))
