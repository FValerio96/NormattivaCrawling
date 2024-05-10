import os

from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from colorama import Fore, Style
from ElencoAtti import startingPageLinkToArrayElencoAtti
from GestioneDataset import check_or_create_jsonl_file
from NormattivaCrawler import startingPageLinkToArray
from Crawler import Crawler
import fileManager

'''
this method takes every act in a range of years, and for every act find any article.
starting_year is the lower 
ending_year is the higher
'''
def crawling_per_anni(starting_year, ending_year):
    '''CREAZIONE CRAWLER'''
    chromedriver_path = 'chrome/chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
    driver = webdriver.Chrome(options=chrome_options)

    '''
    !!!AD OGNI NUOVO ANNO RICORDA DI MODIFICARE IL NOME DEL FILE!!!
    '''
    crawler = Crawler(
        driver=driver,
        url='https://www.normattiva.it/ricerca/elencoPerData/anno/2016?tabID=0.06629760683032282&title=lbl.risultatoRicerca',
        json_file_path=check_or_create_jsonl_file("from " + str(ending_year) + " to " +str(starting_year) + " elenco atti.jsonl")
    )
    #se links è pieno vuol dire che il sw si è bloccato e stai riavviando quindi non prelevo i link
    if(os.path.getsize("links.txt") == 0):
        starting_url = "https://www.normattiva.it/ricerca/elencoPerData"
        Starting_links = startingPageLinkToArrayElencoAtti(starting_url, starting_year, ending_year)
        for link in Starting_links:
            crawler.driver.delete_all_cookies()
            crawler.setNewUrl(link)
            crawler.prelievo_atti()

    links = fileManager.load_links_from_file("Links.txt")
    tot_links = len(links)
    links_visited = 0

    with open("info.txt", "a") as info:
        info.write("numero articoli iniziale: " + str(tot_links))

    for link in links:
        crawler.setNewUrl(link)
        print("crawling of " + link)
        try:
            crawler.acquisisci_articoli_da_url()
            fileManager.remove_first_link_from_file("Links.txt")
            links_visited += 1
        except Exception as e:
            print(Exception)

        percentuale = links_visited / tot_links * 100
        print(Fore.MAGENTA + "%link " + str(percentuale) +
              "\nlink visitati: " + str(links_visited) +
              "link totali: " + str(tot_links))
        print(Fore.BLACK)
crawling_per_anni(1983, 1988)