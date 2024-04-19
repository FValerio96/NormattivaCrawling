from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def takeHTMLFromUrl(url, driver):
    try:
        findTextInClassBS(url, "bodyTesto", driver)
        url = driver.current_url
        while articoloSuccessivov2(driver, url):
            time.sleep(4)
            findTextInClassBS(url, "bodyTesto", driver)
            url = driver.current_url


    except Exception as e:
        print("Eccezione: " + e)

    finally:
        print("articoli finiti")
        return driver

'''
taking a list of url to applicate crawling
'''
def takeHTMLFromlinks(links, driver):
    for url in links:
        try:
            findTextInClassBS(url, "bodyTesto", driver)
            url = driver.current_url
            while articoloSuccessivov2(driver, url):
                findTextInClassBS(url, "bodyTesto", driver)
                url = driver.current_url


        except:
            print("Eccezione")

        finally:
            print("articoli finiti")

def findTextInClassBS(url, className, driver):
    # Effettua la richiesta GET alla pagina
    driver.get(url)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')

    # Trova il div con la classe specificata
    div_container = soup.find('div', class_=className)

    # Stampare il contenuto del div
    if div_container:
        print(div_container.get_text())
    else:
        print("Nessun div con la classe"+ className + " nella pagina.")


def articoloSuccessivov2(driver, url):
    try:
        # Attendere fino a quando almeno due link non sono cliccabili (presenti nella pagina)
        #ciò si  basa sul fatto che il secondo link è articolo successivo
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="btn"]'))
        )

        linkToClick = None

        for link in links:
            if link.accessible_name == "articolo successivo":
                linkToClick = link
                break

        if linkToClick.accessible_name == "articolo successivo":
            print("trovato prossimo link da seguire, clicclo " + linkToClick.accessible_name)
            linkToClick.click()
            return True

        else:
            print("Non ci sono altri link 'articolo successivo' nella pagina")
            #e quindi possiamo fermarci.
            return False
    except Exception as e:
        print("Errore durante il clic sul link:", e)
        return False



# Percorso del driver Chrome
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
# Inizializza il driver di Chrome
driver = webdriver.Chrome(options=chrome_options)
takeHTMLFromUrl('https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:regio.decreto:1940-10-28;1443', driver)

