import time

import requests
from bs4 import BeautifulSoup

# URL della pagina
url = "https://www.normattiva.it/staticPage/codici"

'''
this method capture link in <div class = col-12 col-sm-12 col-md-9 col-lg-9 col-xl-9 pl-4> 
in the starting page.
'''
def startingPageLinkToArray(url):
    # Effettua la richiesta GET alla pagina
    response = requests.get(url)
    links = []

    # Verifica se la richiesta ha avuto successo
    if response.status_code == 200:
        # Parsing del contenuto HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trova il div con la classe d'interesse
        div_container = soup.find('div', class_='col-12 col-sm-12 col-md-9 col-lg-9 col-xl-9 pl-4')

        for link in div_container.find_all('a'):
            # Ottieni l'attributo 'href' del tag 'a'
            link_url = link.get('href')
            # il link è un uri relativo, lo concateno alla homepage per ottenere il path assoluto.
            links.append("https://www.normattiva.it" + link_url)


        print("Links trovati:")
        for link in links:
            print(link)



    else:
        print("Errore nella richiesta HTTP:", response.status_code)

    return links


'''
this method take the text in <div class = "bodyTesto"> form the passed url
'''
def takeBodyTextFromUrl(url):
    # Effettua la richiesta GET alla pagina
    response = requests.get(url)
    retries = 3
    backoff_factor = 0.5
    for i in range (retries):
        # Verifica se la richiesta ha avuto successo
        if response.status_code == 200:
            # Parsing del contenuto HTML
            soup = BeautifulSoup(response.content, 'html.parser')

            # Trova il div con la classe specificata
            div_container = soup.find('div', class_='bodyTesto')

            # Stampare il contenuto del div
            if div_container:
                print(div_container.get_text())
            else:
                print("Nessun div con la classe 'bodyTesto' trovato nella pagina.")
                time.sleep(backoff_factor * (2 ** i))
        else:
            print("Errore nella richiesta HTTP:", response.status_code)


#links = startingPageLinkToArray(url)

