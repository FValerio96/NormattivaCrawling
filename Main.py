from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from ElencoAtti import startingPageLinkToArrayElencoAtti
from GestioneDataset import check_or_create_jsonl_file
from NormattivaCrawler import startingPageLinkToArray
from Selenium import Crawler

def write_links_to_file(links, filename):
    with open(filename, 'a') as f:
        for link in links:
            f.write(link + '\n')

def load_links_from_file(filename):
    with open(filename, 'r') as f:
        links = f.readlines()
        links = [link.strip() for link in links]
        return links

def remove_first_link_from_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        f.writelines(lines[1:])



'''

url = "https://www.normattiva.it/staticPage/codici"
#links = startingPageLinkToArray(url)

'''


''' PRELIEVO ARTICOLI'''

'''
genera tutti i link per gli atti e li scrive su un file links.txt
'''
def prelievo_atti(crawler):
    crawler.conta_numero_atti()
    next_page = 2
    links = crawler.prendi_link_in_div()
    write_links_to_file(links, "links.txt")  # Scrivi i link su file
    while crawler.clicca_pagina_successiva(next_page):
        next_page += 1
        links = crawler.prendi_link_in_div()
        write_links_to_file(links, "links.txt")  # Scrivi i link su file


'''
legge dal file links.txt i link, per ognuno dei quali andrà a scaricare tutti gli articoli
'''
def prelievo_ariticoli():
    # in links contengo tutti i link degli atti
    linksAtti = load_links_from_file("Links.txt")
    # per ogni atto itero
    for link in linksAtti:
        #sposto il crawler sul nuovo link
        crawler.setNewUrl(link)
        print("crawling of " + link)
        try:
            #prendo tutti gli articoli nel link
            crawler.acquisisci_articoli_da_url()
            remove_first_link_from_file("Links.txt")
        except Exception as e:
            print(Exception)


'''CREAZIONE CRAWLER'''
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
driver = webdriver.Chrome(options=chrome_options)
'''
!!!AD OGNI NUOVO ANNO RICORDA DI MODIFICARE IL FILE!!!
'''
jsonl_file_path = check_or_create_jsonl_file("from 2014 to 2004 elenco atti.jsonl")
crawler = Crawler(
    driver=driver,
    url='https://www.normattiva.it/ricerca/elencoPerData/anno/2016?tabID=0.06629760683032282&title=lbl.risultatoRicerca',
    json_file_path='json_file.json'
)

starting_url = "https://www.normattiva.it/ricerca/elencoPerData"
Starting_links = startingPageLinkToArrayElencoAtti(starting_url)
#to update: fai scrivere tra un link e l'altro nel jsonL un commento con l'anno in modo da poter ispezionare
for link in Starting_links:
    crawler.driver.get(link)
    time.sleep(4)
    prelievo_atti(crawler)