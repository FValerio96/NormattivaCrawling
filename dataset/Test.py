from ElencoAtti import startingPageLinkToArray
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from Selenium import Crawler

#prendo i link
links = []
starting_url = "https://www.normattiva.it/ricerca/elencoPerData"
links = startingPageLinkToArray(starting_url)

# preparo il driver
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
driver = webdriver.Chrome(options=chrome_options)

link = links[0]

crawler = Crawler(driver = driver, url = link, json_file_path = None)
print("crawling of " + link)
while(crawler.scorrimento_pagina_articoli()):
    print(crawler.driver.current_url)


