import os

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from colorama import Fore
from utils.utils import startingPageLinkToArrayElencoAtti
from utils import fileManager
from dataset.gestioneDataset import check_or_create_jsonl_file
from crawling.Crawler import Crawler

italgiure_url = "https://www.italgiure.giustizia.it/sncass/"

def crawler_creations():

    '''CREAZIONE CRAWLER'''
    chromedriver_path = 'chrome/chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    crawler = Crawler(
        driver=driver,
        url=italgiure_url,
        json_file_path="italgiure"
    )

    return crawler

crawler = crawler_creations()
crawler.trova_complementary_e_stampa()
crawler.trova_complementary_e_clicca2()
crawler.clicca_pdf()