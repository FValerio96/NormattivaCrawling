import json
from selenium.common import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
import time
from datetime import datetime
import re
from utils import fileManager


class Crawler:
    def __init__(self, driver, url, json_file_path, className: str="bodyTesto"):
        self.driver: WebDriver = driver
        # go to the url
        self.setNewUrl(url)
        self.jsonl_file_path = json_file_path
        self.lastRowInserted = None
        self.className: str = className

    def acquisisci_articoli_da_url(self):
        try:
            continueCrawling = True
            self.trova_testo_in_classe_BS()
            #se cado nel loop di articolo successivo con rimando a se stesso vado al prossimo link
            #dopo aver visionato centinaia di pagine ciò è accaduto solo nell'ultimo articolo dei link.
            while continueCrawling:
                continueCrawling = self.articoloSuccessivov2()

        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt
            print("Eccezione: ", e + " URL: " + self.driver.current_url)

        finally:
            print("articoli finiti")

    def articoloSuccessivov2(self):
        timeout = 0
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
                    print('Timeout: ', timeout, "and url: ", self.driver.current_url)

                for link in links:
                    if link.accessible_name == "articolo successivo":
                        linkToClick = link
                        break

            # se è avvalorato è avvalorato con articolo successivo
                if linkToClick is not None:
                    print("trovato prossimo link da seguire, clicco " , linkToClick.accessible_name)
                    linkToClick.click()
                    time.sleep(1)
                    continueCrawling = self.trova_testo_in_classe_BS()

                    if continueCrawling:
                        return True
                else:
                    print("Non ci sono altri link 'articolo successivo' nella pagina")
                # e quindi possiamo fermarci.
            return False
        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt
            print("Errore durante il clic sul link:", e)
            print('Timeout: ', timeout, "and url: ", self.driver.current_url)
            return False

    def trova_testo_in_classe_BS(self):
        try:
            text_content = None
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            pageSource = self.driver.page_source
            soup = BeautifulSoup(pageSource, 'html.parser')

            # Trova il div con la classe specificata
            div_container = soup.find('div', class_=self.className)

            # Stampare il contenuto del div
            if div_container:
                text_content = div_container.get_text()
            else:
                print("Nessun div con la classe" + self.className + " nella pagina.")

            # Se text_content non è vuoto, procedi con la creazione del JSON ed il suo inserimento nel JSONL
            if text_content is not None:
                # Crea il file JSON con i campi richiesti
                json_data = {
                    "text": text_content,
                    "url": self.driver.current_url,
                    "source": "normattiva",
                    "timestamp": datetime.now().isoformat()
                }

                if self.lastRowInserted is not None:
                    if self.lastRowInserted != text_content:
                        self.scrivi_articolo(json_data, text_content)
                        return True
                    else:
                        print("articolo gia inserito")
                else:
                    self.scrivi_articolo(json_data, text_content)
                    return True
            else:
                print("no text in page: ", self.driver.current_url)
            return False
        except Exception as e:
            print("findText exception : ", e.__str__())

    def scrivi_articolo(self, json_data, text_content):
        with open(self.jsonl_file_path, "a") as jsonl_file:
            json.dump(json_data, jsonl_file)
            jsonl_file.write("\n")

        self.lastRowInserted = text_content
        return True



    def setNewUrl(self, url):
        self.driver.get(url)
        print("il driver si sposta su " + url)


    '''
    this method return the number of article in page
    '''
    def conta_numero_atti(self):
        text_content = None
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        pageSource = self.driver.page_source
        soup = BeautifulSoup(pageSource, 'html.parser')

        # Trova il div con la classe specificata
        div_container = soup.find('div', class_="col-12 box paginatore_info py-2")

        # Stampare il contenuto del div
        if div_container:
            # capisco il numero di articoli
            text_content = div_container.get_text()
            numero_articoli = (re.search(r'\d+', text_content))
            if numero_articoli:
                numero_articoli = int(numero_articoli.group())
            print("il numero degli atti è: " + str(numero_articoli))
            # sapendo che il contenuto delle pagine è di max 20 divido numero_articoli per 20,
            # arrrotondo (eventualmente) per eccesso ed ho il numero di pagine.
            pageNumber = int(numero_articoli / 20)
            # se serve faccio l'arrotondamento
            if numero_articoli % 20 != 0:
                pageNumber += 1
            print("ci sono " + str(pageNumber) + " pagine")
        else:
            numero_articoli = 0
        return numero_articoli

    '''
    this method find every link in the specific div and return the number of link.
    '''

    def prendi_link_in_div(self):
        try:
            div_xpath = '//div[contains(@class, "col-12") and contains(@class, "col-sm-12") and contains(@class, "col-md-12") and contains(@class, "col-lg-8") and contains(@class, "col-xl-8") and contains(@class, "box risultato")]'

            # Trova il div con la classe specificata
            div_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, div_xpath))
            )

            # Trova tutti gli elementi <a> all'interno del div
            links = div_element.find_elements(By.TAG_NAME, 'a')

            # Salva gli attributi href di tutti i link trovati in una lista
            lista_link = []
            for link in links:
                href = link.get_attribute('href')
                if href:
                    lista_link.append(href)

            # Restituisci il numero di link trovati
            return lista_link

        except TimeoutException:
            print("Div non trovato entro il timeout")
            return []


    def clicca_pagina_successiva(self, next_page):
        try:
            linkToClick: WebElement | None = None
            links = None
            allTimeout = [10, 20, 30, 50, 60]
            for timeout in allTimeout:
                try:
                    link_xpath = f'//a[@class="page-link" and text()="{str(next_page)}"]'
                    # Trova il link con il numero di pagina specificato
                    link_element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, link_xpath))
                    )


                except Exception as e:
                    if isinstance(e, KeyboardInterrupt):
                        raise KeyboardInterrupt

                    print('Timeout: ', timeout + "and url: " + self.driver.current_url)
                if link_element.accessible_name == str(next_page):
                    # Clicca sul link
                    link_element.click()
                    next_page += 1
                    print(f"Link alla pagina {next_page} trovato e cliccato.")
                    return True
                else:
                    print("Link non trovato")
                    return False


        except Exception as e:
            if isinstance(e, KeyboardInterrupt):
                raise KeyboardInterrupt
            print("Errore durante il clic sul link:", e)
            print('Timeout: ', str(timeout) + "and url: " + self.driver.current_url)
            return False


    def scorrimento_pagina_articoli(self, numero_articoli):
        currentPage = 1
        links = self.prendi_link_in_div()
        self.clicca_pagina_successiva(currentPage)
        currentPage += 1
        while numero_articoli > len(links):
            links.append(self.prendi_link_in_div())
            # devo spostarmi alla pagina successiva
            currentPage += 1
            self.clicca_pagina_successiva(currentPage)

        for link in links:
            print(link)
        else:
            print("Nessun div con la classe col-12 box paginatore_info py-2 nella pagina.")

    '''
    genera tutti i link per gli atti e li scrive su un file links.txt
    '''

    def prelievo_atti(self):
        self.conta_numero_atti()
        next_page = 2
        links = self.prendi_link_in_div()
        fileManager.write_links_to_file(links, "../links.txt")  # Scrivi i link su file
        while self.clicca_pagina_successiva(next_page):
            next_page += 1
            links = self.prendi_link_in_div()
            fileManager.write_links_to_file(links, "links.txt")  # Scrivi i link su file

    '''
    legge dal file links.txt i link, per ognuno dei quali andrà a scaricare tutti gli articoli
    '''
    def prelievo_ariticoli(self):
        # in links contengo tutti i link degli atti
        linksAtti = fileManager.load_links_from_file("../links.txt")
        # per ogni atto itero
        for link in linksAtti:
            # sposto il crawler sul nuovo link
            self.setNewUrl(link)
            print("crawling of " + link)
            try:
                # prendo tutti gli articoli nel link
                self.acquisisci_articoli_da_url()
                fileManager.remove_first_link_from_file("./links.txt")
            except Exception as e:
                print(Exception)

    '''
    NEW METHODS FOR ITALGIURE'S SCRAPING
    '''

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException

    '''
        con questo metodo ricerco la zona di interesse sulla a sx, quello che si presenta come un menù a tendina
        in realtà è una cella di una tabella riconoscibile attraverso l'attributo role
    '''
    def trova_complementary_e_stampa(self):
        self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        try:
            # Trova il <td> con role="complementary"
            print("Cercando il <td> con role='complementary'...")
            td_complementary = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//td[@role="complementary"]'))
            )
            if td_complementary:
                print("<td> con role='complementary' trovato.")

                # Trova tutti i <span> con class="keyIgnore" all'interno del <td>
                spans = td_complementary.find_elements(By.XPATH, './/span[@class="keyIgnore"]')
                if spans:
                    print(f"Trovati {len(spans)} elementi <span> con class='keyIgnore':")
                    for span in spans:
                        # Stampa il testo all'interno del <span>
                        print(span.text.strip())
                else:
                    print("Nessun elemento <span> con class='keyIgnore' trovato.")
            else:
                print("<td> con role='complementary' non trovato.")

        except TimeoutException:
            print("Non è stato possibile trovare il <td> con role='complementary' entro il tempo limite.")
        except Exception as e:
            print(f"Errore: {str(e)}")

    '''
    = al metodo precedente ma clicca
    '''
    def trova_complementary_e_clicca2(self):
        #svuoto la cache altrimeti non funziona
        self.driver.execute_cdp_cmd('Network.clearBrowserCache', {})
        try:
            # Trova il <td> con role="complementary"
            print("Cercando il <td> con role='complementary'...")
            td_complementary = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//td[@role="complementary"]'))
            )
            if td_complementary:
                print("<td> con role='complementary' trovato.")

                # Trova tutti i <span> con class="keyIgnore" all'interno del <td>
                spans = td_complementary.find_elements(By.XPATH, './/span[@class="keyIgnore"]')
                if spans:
                    print(f"Trovati {len(spans)} elementi <span> con class='keyIgnore':")
                    for span in spans:
                        # Stampa il testo all'interno del <span>
                        span_text = span.text.strip()
                        print(f"Testo trovato: {span_text}")

                        # Clicca sul <span>
                        print(f"Cliccando su: {span_text}")
                else:
                    print("Nessun elemento <span> con class='keyIgnore' trovato.")
            else:
                print("<td> con role='complementary' non trovato.")

        except TimeoutException:
            print("Non è stato possibile trovare il <td> con role='complementary' entro il tempo limite.")
        except Exception as e:
            print(f"Errore: {str(e)}")


    '''probabilmente inutile'''
    def clicca_civile(self):
        try:
            print("Cercando il tag <tbody> nella tabella con ID 'facets'...")
            # Trova il tag <tbody> all'interno della tabella con ID "facets"
            tbody = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//table[@id="facets"]/tbody'))
            )
            if tbody:
                print("<tbody> trovato!")

                # Cerca l'elemento "CIVILE" all'interno del <tbody>
                print("Cercando l'elemento con testo 'CIVILE'...")
                civile_element = tbody.find_element(By.XPATH, './/span[@class="keyIgnore" and text()="CIVILE"]')

                if civile_element:
                    print("Elemento 'CIVILE' trovato. Cliccando...")
                    civile_element.click()
                else:
                    print("Elemento 'CIVILE' non trovato all'interno del <tbody>.")

        except TimeoutException:
            print("Non è stato possibile trovare il <tbody> o l'elemento 'CIVILE' entro il tempo limite.")
        except Exception as e:
            print(f"Errore durante il clic su 'CIVILE': {str(e)}")

    '''
    not works
    '''
    def clicca_pdf(self):
        try:
            # Trova tutti gli elementi che rappresentano i PDF nel box
            pdf_links = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[@class="results"]//a[contains(@href, ".pdf")]'))
            )

            # Itera su ciascun link e clicca
            for pdf_link in pdf_links[:10]:  # Limita ai primi 10 PDF
                href = pdf_link.get_attribute("href")  # Trova l'URL del PDF
                print(f"Sto cliccando sul link PDF: {href}")
                pdf_link.click()

                # Aspetta un momento per assicurarti che l'azione venga eseguita
                WebDriverWait(self.driver, 10).until(
                    EC.url_changes(self.driver.current_url)
                )

                # Torna indietro se necessario
                self.driver.back()
        except Exception as e:
            print("Errore durante il clic sui PDF:", str(e))






