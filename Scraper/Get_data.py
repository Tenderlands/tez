import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


def handle_sentence(sentence):
    sentence = " ".join(sentence.strip().split())
    return sentence


r = open(os.path.join(os.getcwd(),'data','new_numbers.txt'), 'r')
att = ["Fiyat","Marka","Seri","Model","Yıl","Yakıt","Vites","KM","Kasa_Tipi","Motor_Gucu","Motor_Hacmi","Cekis","Renk","Garanti","Plaka","Kimden","Takas","Arac_Durum"]
df = pd.DataFrame(columns=att)

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

counter = 0
line = r.readline().strip()
while line != "":
    url = 'http://www.sahibinden.com/ilan/'+line+'/detay'
    try:
        link = requests.get(url, headers=headers)
    except:
        line = r.readline().strip()
        continue
    page = BeautifulSoup(link.content, "lxml")
    content = page.find_all('div', attrs={'class': 'classifiedInfo'})
    current = []
    try:
        fiyat = str(content[0].find_all('h3')[0].next_element)
        current.append(handle_sentence(fiyat))
        attrs = content[0].find_all('span')
        for i in range(9, 26):
            try:
                current.append(handle_sentence(attrs[i].text))
            except Exception as e:
                print('error: ' + str(e))
                break
        df.loc[counter] = current
        counter += 1
    except Exception as e:
        print('error: ' + str(e))
    line = r.readline().strip()
    time.sleep(0.7)

if os.path.exists('dataframe.csv'):
    old_df = pd.read_csv('dataframe.csv')
    old_df.append(df)
    old_df.to_csv('dataframe.csv')
else:
    df.to_csv('dataframe.csv')

w = open(os.path.join(os.getcwd(),'data','old_numbers.txt'), 'a')
try:
    w.write(r.read())
    r.close()
    os.remove(os.path.join(os.getcwd(),'data','new_numbers.txt'))
except:
    pass

