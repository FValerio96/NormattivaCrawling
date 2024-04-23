import json

from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
import time
from datetime import datetime

class Crawler:
    def __init__(self, driver, url, json_file_path):
        self.driver: WebDriver = driver
        # go to the url
        self.setNewUrl(url)
        self.jsonl_file_path = json_file_path
        self.lastRowInserted = None


    def takeHTMLFromUrl(self):
        try:
            self.findTextInClassBS("bodyTesto")

            while self.articoloSuccessivov2():
                time.sleep(4)
                self.findTextInClassBS("bodyTesto")

        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt
            print("Eccezione: ", e + " URL: " + self.driver.current_url)

        finally:
            print("articoli finiti")


    def findTextInClassBS(self, className):
        text_content = None
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        pageSource = self.driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')

        # Trova il div con la classe specificata
        div_container = soup.find('div', class_=className)

        # Stampare il contenuto del div
        if div_container:
            text_content = div_container.get_text()
        else:
            print("Nessun div con la classe" + className + " nella pagina.")

        # Se text_content non è vuoto, procedi con la creazione del JSON ed il suo inserimento nel JSONL
        if text_content is not None:
            # Crea il file JSON con i campi richiesti
            json_data = {
                "text": text_content,
                "url": self.driver.current_url,
                "source": "normattiva",
                "timestamp": datetime.now().isoformat()
            }

            if self.lastRowInserted is None or self.lastRowInserted != text_content:
                with open(self.jsonl_file_path, "a") as jsonl_file:
                    json.dump(json_data, jsonl_file)
                    jsonl_file.write("\n")

                self.lastRowInserted = text_content

            else:
                print('Articolo già inserito')
    def articoloSuccessivov2(self):
        try:
            linkToClick: WebElement | None = None

            links = None
            allTimeout = [10, 20, 30, 50, 60]

            # Attendere fino a quando almeno due link non sono cliccabili (presenti nella pagina)
            # ciò si  basa sul fatto che il secondo link è articolo successivo
            for timeout in allTimeout:
                print('Esecuzione con timeout: ', timeout)
                try:
                    links = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="btn"]'))
                    )

                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise KeyboardInterrupt
                    print('Timeout: ', timeout + "and url: " + self.driver.current_url)

                for link in links:
                    if link.accessible_name == "articolo successivo":
                        linkToClick = link
                        break

                if linkToClick is not None:
                    break
            #se è avvalorato è avvalorato con articolo successivo
            if linkToClick is not None:
                print("trovato prossimo link da seguire, clicco " + linkToClick.accessible_name)
                linkToClick.click()
                return True

            else:
                print("Non ci sono altri link 'articolo successivo' nella pagina")
                # e quindi possiamo fermarci.
                return False
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt
            print("Errore durante il clic sul link:", e)
            print('Timeout: ', timeout + "and url: " + self.driver.current_url)
            return False

    def setNewUrl(self, url):
        self.driver.get(url)

    def paginaSuccessiva(self):
        pageNumber = 2
        pageNumberString = "2"
        try:
            linkToClick: WebElement | None = None

            links = None
            allTimeout = [10, 20, 30, 50, 60]

            for timeout in allTimeout:
                print('Esecuzione con timeout: ', timeout)
                try:
                    links = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_all_elements_located((By.XPATH, '//a[@class="btn"]'))
                    )

                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise KeyboardInterrupt
                    print('Timeout: ', timeout + "and url: " + self.driver.current_url)

                for link in links:
                    if link.accessible_name == pageNumber or link.accessible_name == pageNumberString:
                        linkToClick = link
                        break

                if linkToClick is not None:
                    pageNumber = pageNumber + 1
                    break
            #se è avvalorato è avvalorato con articolo successivo
            if linkToClick is not None:
                print("trovato prossimo link da seguire, clicco " + linkToClick.accessible_name)
                linkToClick.click()
                return True

            else:
                print("Non ci sono altri link 'articolo successivo' nella pagina")
                # e quindi possiamo fermarci.
                return False
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt
            print("Errore durante il clic sul link:", e)
            print('Timeout: ', timeout + "and url: " + self.driver.current_url)
            return False

'''

# Percorso del driver Chrome
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
# Inizializza il driver di Chrome
driver = webdriver.Chrome(options=chrome_options)
# jsonl_file_path = check_or_create_jsonl_file()
crawler = Crawler(
    driver=driver,
    url='https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:regio.decreto:1930-10-19;1398',
    json_file_path='json_file.json'
)
crawler.takeHTMLFromUrl()

'''


