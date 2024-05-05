from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from GestioneDataset import check_or_create_jsonl_file
from Crawler import Crawler


chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
driver = webdriver.Chrome(options=chrome_options)

jsonl_file_path = check_or_create_jsonl_file("from 2014 to 2004 elenco atti.jsonl")
crawler = Crawler(
    driver=driver,
    url='https://chat.openai.com/',
    json_file_path='json_file.json'
)

crawler.setNewUrl("https://www.milannews.it/")
crawler.setNewUrl("https://github.com/")