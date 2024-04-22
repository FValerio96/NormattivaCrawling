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



url = "https://www.normattiva.it/staticPage/codici"
links = startingPageLinkToArray(url)
jsonl_file_path = check_or_create_jsonl_file()

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

