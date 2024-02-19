import requests
from bs4 import BeautifulSoup
import pprint

link = 'https://www.bankier.pl/waluty'
req = requests.get(link)
bankier_html = BeautifulSoup(req.text, 'html.parser')

title_div = bankier_html.select('#boxKursyNbp')
rates_div = bankier_html.select('#boxKursyNbpTab1 > table > tbody')

def get_rates(title_div, rates_div):
    rates_list = []
    title = title_div[0].find('div').find('h2').getText()
    rates_list.append({'source_title': title})
    rates_list.append({'source_link': link})
    names = rates_div[0].select('.name')[::2]
    for i in range(len(rates_div[0].find_all('tr'))):
        name = names[i].select('a')[0].getText()
        value = rates_div[0].select('.value')[i].getText()
        rates_list.append({'name': name,
                           'value': value})
    return rates_list

pprint.pprint(get_rates(title_div, rates_div))

