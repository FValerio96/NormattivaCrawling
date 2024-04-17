import requests
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def takeHTMLFromUrl(url, driver):

    try:
        findTextInClassBS(url, "bodyTesto", driver)
        url = driver.current_url
        while articoloSuccessivov2(driver, url):
            findTextInClassBS(url, "bodyTesto", driver)
            url = driver.current_url


    except:
        print("Eccezione")



def findTextInClassBS(url, className, driver):
    # Effettua la richiesta GET alla pagina
    driver.get(url)

    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')

    # Trova il div con la classe specificata
    div_container = soup.find('div', class_=className)

    # Stampare il contenuto del div
    if div_container:
        print(div_container.get_text())
    else:
        print("Nessun div con la classe"+ className + " nella pagina.")

def articoloSuccessivo(driver, url):
    # Attendere fino a quando il link non è cliccabile (presente nella pagina)
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@class="btn"]'))
    )
    link.click()


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def articoloSuccessivov2(driver, url):
    try:
        # Attendere fino a quando almeno due link non sono cliccabili (presenti nella pagina)
        links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//a[@class="btn"]'))
        )

        # Se ci sono almeno due link, clicca sul secondo link
        if len(links) >= 2:
            links[1].click()
        else:
            print("Non ci sono abbastanza link 'articolo successivo' nella pagina")
        return True
    except Exception as e:
        print("Errore durante il clic sul link:", e)
        return False


def get_number_of_ArticoloSuccessivo(className, url):
    try:
        # Effettua una richiesta GET all'URL
        response = requests.get(url)

        # Verifica se la richiesta ha avuto successo
        if response.status_code == 200:
            # Parsa il contenuto HTML della pagina con BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Trova l'elemento con la classe specificata
            target_element = soup.find('div', class_=className)

            # Verifica se l'elemento è stato trovato
            if target_element:
                # Trova l'unordered list all'interno dell'elemento trovato
                ul = target_element.find('ul')

                # Conta il numero di elementi <li> all'interno dell'unordered list
                if ul:
                    number_of_items = len(ul.find_all('li'))
                    return number_of_items
                else:
                    print("Nessun unordered list trovato all'interno dell'elemento con classe", className)
            else:
                print("Nessun elemento trovato con classe", className)
        else:
            print("Errore durante la richiesta GET:", response.status_code)
    except Exception as e:
        print("Errore durante l'analisi della pagina:", e)

'''
                MAIN
'''
get_number_of_ArticoloSuccessivo("allegati_lista", "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:costituzione")

# Percorso del driver Chrome
chromedriver_path = 'chrome/chromedriver.exe'
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("webdriver.chrome.driver=" + chromedriver_path)
# Inizializza il driver di Chrome
driver = webdriver.Chrome(options=chrome_options)
takeHTMLFromUrl('https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:costituzione', driver)

