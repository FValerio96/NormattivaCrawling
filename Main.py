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
from Crawler import Crawler
import fileManager


'''CREAZIONE CRAWLER'''
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
driver = webdriver.Chrome(options=chrome_options)
'''
!!!AD OGNI NUOVO ANNO RICORDA DI MODIFICARE IL FILE!!!
'''

crawler = Crawler(
    driver=driver,
    url='https://www.normattiva.it/ricerca/elencoPerData/anno/2016?tabID=0.06629760683032282&title=lbl.risultatoRicerca',
    json_file_path=check_or_create_jsonl_file("from 2014 to 2012 elenco atti.jsonl")
)

starting_url = "https://www.normattiva.it/ricerca/elencoPerData"
Starting_links = startingPageLinkToArrayElencoAtti(starting_url)

for link in Starting_links:
    crawler.driver.delete_all_cookies()
    crawler.setNewUrl(link)
    crawler.prelievo_atti()


links = fileManager.load_links_from_file("Links.txt")

for link in links:
    crawler.setNewUrl(link)
    print("crawling of " + link)
    try:
        crawler.acquisisci_articoli_da_url()
        fileManager.remove_first_link_from_file("Links.txt")
    except Exception as e:
        print(Exception)