from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from NormattivaCrawler import startingPageLinkToArray
from Selenium import takeHTMLFromUrl, takeHTMLFromlinks

url = "https://www.normattiva.it/staticPage/codici"
links = startingPageLinkToArray(url)

# Percorso del driver Chrome
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
# Inizializza il driver di Chrome
driver = webdriver.Chrome(options=chrome_options)

for link in links:
    print("crawling of " + link)
    takeHTMLFromUrl(link, driver)

