from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

links = load_links_from_file("Links.txt")
for link in links:
    print(link)

url = "https://www.normattiva.it/staticPage/codici"
#links = startingPageLinkToArray(url)
jsonl_file_path = check_or_create_jsonl_file()
#write_links_to_file(links, "Links.txt")

# Percorso del driver Chrome
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
# Inizializza il driver di Chrome
driver = webdriver.Chrome(options=chrome_options)

for link in links:
    crawler = Crawler(driver = driver, url = link, json_file_path = jsonl_file_path)
    print("crawling of " + link)
    crawler.takeHTMLFromUrl()
    remove_first_link_from_file("Links.txt")
'''


chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
driver = webdriver.Chrome(options=chrome_options)
# jsonl_file_path = check_or_create_jsonl_file()
crawler = Crawler(
    driver=driver,
    url='https://www.normattiva.it/ricerca/elencoPerData/anno/2015?tabID=0.2985707928192325&title=lbl.risultatoRicerca',
    json_file_path='json_file.json'
)

numero_articoli = crawler.conta_numero_articoli()
next_page = 2
links = crawler.prendi_link_in_div()
write_links_to_file(links, "links.txt")  # Scrivi i link su file
while (crawler.clicca_pagina_successiva(next_page)) :
    next_page +=1
    links = crawler.prendi_link_in_div()
    write_links_to_file(links, "links.txt")  # Scrivi i link su file


links = load_links_from_file("Links.txt")
for link in links:
    print(link)
