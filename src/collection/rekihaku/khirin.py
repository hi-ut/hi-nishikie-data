import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

page = 0

flg = True

while flg:
    url = "http://khirin-a.rekihaku.ac.jp/search?kywd=%E9%8C%A6%E7%B5%B5&page={}".format(page)

    print(url)

    r = requests.get(url,timeout=30)

    soup = BeautifulSoup(r.text, "html.parser")

    name = 'data/歴博/{}.csv'.format(str(page).zfill(4))

    '''
    df = pd.read_csv(io.BytesIO(r.content),sep=",")

    df.to_csv('data/歴博/{}.csv'.format(str(page).zfill(4)))
    '''

    with open(name, mode='w') as f:
        f.write(str(soup))

    page += 1

    if page > 101:
        flg = False
