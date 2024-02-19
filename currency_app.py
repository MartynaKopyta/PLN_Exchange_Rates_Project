from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    link = 'https://www.bankier.pl/waluty'
    req = requests.get(link)
    bankier_html = BeautifulSoup(req.text, 'html.parser')

    title_div = bankier_html.select('#boxKursyNbp')
    rates_div = bankier_html.select('#boxKursyNbpTab1 > table > tbody')

    rates_list = get_rates(title_div, rates_div)
    return render_template('index.html', rates=rates_list)

def get_rates(title_div, rates_div):
    rates_list = []
    title = title_div[0].find('div').find('h2').getText()
    rates_list.append({'source_title': title})
    rates_list.append({'source_link': 'https://www.bankier.pl/waluty'})
    names = rates_div[0].select('.name')[::2]
    for i in range(len(rates_div[0].find_all('tr'))):
        name = names[i].select('a')[0].getText()
        value = rates_div[0].select('.value')[i].getText()
        rates_list.append({'name': name,
                           'value': value})
    return rates_list

if __name__ == '__main__':
    app.run(debug=True)
