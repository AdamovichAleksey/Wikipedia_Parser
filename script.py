import sys

try:
    f = open(sys.argv[1], 'r')
    f.close()
except OSError:
    print('cannot open ', sys.argv[1])
    raise
    
from bs4 import BeautifulSoup
from urllib.request import urlopen 
from pandas import read_csv, DataFrame

df = read_csv(sys.argv[1], names = ['wikipedia_page', 'website'])

def get_direct_link(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    try:
        return soup.find_all('span', 'url')[-1].find_all('a', 'external')[-1].get('href')   
    except Exception:
        return soup.find_all('a', 'external')[0].get('href')
    
for i, row in df.iterrows():
    df.loc[i, 'website'] = get_direct_link(row['wikipedia_page'])
    
df.to_csv('answer.csv', index = False)
