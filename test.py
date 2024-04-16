from telnetlib import EC

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def find_showArticle_links(url):
    # Effettua la richiesta GET alla pagina
    response = requests.get(url)
    showArticle_links = []

    # Verifica se la richiesta ha avuto successo
    if response.status_code == 200:
        # Parsing del contenuto HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trova tutte le chiamate alla funzione showArticle
        showArticle_calls = soup.find_all(lambda tag: tag.name == 'a' and 'showArticle' in tag.get('onclick', ''))
        # Estrai gli argomenti dalla chiamata alla funzione showArticle
        for call in showArticle_calls:
            # Ottieni l'argomento dalla chiamata onclick
            onclick_value = call.get('onclick')
            start_index = onclick_value.find("(") + 1
            end_index = onclick_value.find(")")
            argument = onclick_value[start_index:end_index].strip("'")  # Rimuovi eventuali apici singoli
            print(argument)
            # Costruisci l'URL completo e aggiungilo alla lista
            full_url = urljoin("https://www.normattiva.it/", argument)
            showArticle_links.append(full_url)

    else:
        print("Errore nella richiesta HTTP:", response.status_code)

    return showArticle_links

