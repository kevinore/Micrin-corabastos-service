from bs4 import BeautifulSoup
import requests
from random import choice
from pymongo import MongoClient
import urllib.parse

G_URL = 'https://www.corabastos.com.co/sitio/historicoApp2/reportes/index.php'

def get_proxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    return {'http':choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text, soup.findAll('td')[::8]),
                                                                    map(lambda x:x.text, soup.findAll('td')[1::8]))))))}

def get_beautilfilSoup(href, **kwargs):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
    proxy = get_proxy()
    resp = requests.get(href,proxies=proxy,headers=headers,verify=False,**kwargs)
    if resp.status_code == 200:
        return BeautifulSoup( resp.text, 'html.parser')
    
def scraping_side():
    soup = get_beautilfilSoup(G_URL)
    if soup is not None:
        username = urllib.parse.quote_plus('kevin')
        password = urllib.parse.quote_plus('@Kevin3132480890')
        
        client = MongoClient("mongodb+srv://%s:%s@corabastos-yqyfv.mongodb.net/test?retryWrites=true&w=majority"%(username,password))
        database = client.Corabastos

        tables = soup.find_all('table',{'class':'table table-bordered table-bordered table-striped table-hover table-condensed'})
        for table in tables:
            items = table.find_all('tr')
            for item in items:
                tds = item.find_all('td')
                if(len(tds) is not 0):
                    jsondata = {'nombre':tds[0].text, 
                                'presentacion':tds[1].text, 
                                'cantidad':tds[2].text, 
                                'unidad':tds[3].text, 
                                'cal_extra':tds[4].text,
                                'cal_primera':tds[5].text,
                                'valorxunidad':tds[6].text}
                    database.items.insert_one(jsondata)
            

if __name__ == '__main__':
    scraping_side()