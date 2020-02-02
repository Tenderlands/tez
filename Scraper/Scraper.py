import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import os


def number_to_int(string):
    string = string.replace(' ilan', '')
    string = string.replace('(', '')
    string = string.replace(')', '')
    string = string.replace('.', '')
    return int(string)


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

att = ['Fiyat', 'Marka', 'Seri', 'Model', 'Yıl', 'Yakıt', 'Vites', 'KM', 'Kasa_Tipi', 'Motor_Gucu', 'Motor_Hacmi',
       'Cekis', 'Renk', 'Garanti', 'Hasar_Durumu', 'Plaka', 'Kimden', 'Takas', 'Arac_Durum']

df = pd.DataFrame(columns=att)

brands = ['fiat', 'ford', 'honda', 'hyundai', 'renault', 'toyota', 'opel', 'volkswagen', 'peugeot']

url_base = 'https://www.sahibinden.com'
#url = url_base + '/otomobil'
#link = requests.get(url, headers=headers)
#content = BeautifulSoup(link.content, 'lxml')
datestr = datetime.now().strftime("%H.%M--%m-%d-%Y")
for brand in brands:

    mode = 'w+'
    if not (os.path.exists('./data/links/'+datestr)):
        os.mkdir('./data/links/'+datestr)
    filename = './data/links/' + datestr + '/' + brand + '.txt'
    f = open(filename, mode)
    url = url_base + '/' + brand
    disconnected = False
    while not disconnected:
        try:
            link = requests.get(url, headers=headers)
            disconnected = True
        except:
            time.sleep(60)
    content = BeautifulSoup(link.content, 'lxml')
    div = content.find('div', attrs={'class': 'result-text'})
    span = div.find('span', attrs={'title': None})
    number = number_to_int(span.text)
    offset = 0
    print(number)
    while offset < 100:
        url = url_base + '/' + brand + '?pagingOffset=' + str(offset) + '&pagingSize=50'
        try:
            link = requests.get(url, headers=headers)
        except:
            time.sleep(60)
            continue
        content = BeautifulSoup(link.content, 'lxml')
        tbody = content.tbody
        links = tbody.findAll('a', attrs={'class': 'classifiedTitle'})
        for l in links:
            lstr = url_base + l['href'] + '\n'
            f.write(lstr)
        offset += 50
        #print(str(number) + ' adet ilanın ' +str(offset) + ' tanesi kaydedildi')
        print('Total Number: ' + str(number) + '  Offset: ' + str(offset))
        time.sleep(0.7)
    f.close()
