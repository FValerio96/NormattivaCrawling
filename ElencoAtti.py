import requests
from bs4 import BeautifulSoup



'''
this method capture link in <div class = col-12 col-sm-12 col-md-9 col-lg-9 col-xl-9 ElencoAnni> 
from 1946 to 2024 in the "elenco atti" page.
'''
def startingPageLinkToArrayElencoAtti(url, starting_year, end_year):
    # Effettua la richiesta GET alla pagina
    response = requests.get(url)
    links = []

    # Verifica se la richiesta ha avuto successo
    if response.status_code == 200:
        # Parsing del contenuto HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Trova il div con la classe d'interesse
        div_container = soup.find('div', class_='col-12 col-sm-12 col-md-9 col-lg-9 col-xl-9 ElencoAnni')

        for link in div_container.find_all('a'):
            link_text = link.get_text().strip()  # Ottieni il testo del link e rimuovi eventuali spazi bianchi in eccesso
            try:
                link_number = int(link_text)
                if link_number >= starting_year and link_number <= end_year:
                    link_url = link.get('href')  # Ottieni l'attributo 'href' del tag 'a'
                    # Il link è un URI relativo, lo concateno alla homepage per ottenere il path assoluto.
                    links.append("https://www.normattiva.it" + link_url)
            except ValueError:
                pass  # Ignora i link il cui testo non può essere convertito in un numero intero

        print("Links trovati:")
        for link in links:
            print(link)

        return links


def yearPageToLink(url):
    # Effettua la richiesta GET alla pagina
    response = requests.get(url)
    links = []
    pageNumber = 1
    # Verifica se la richiesta ha avuto successo
    if response.status_code == 200:
        # Parsing del contenuto HTML
        soup = BeautifulSoup(response.content, 'html.parser')

'''
Starting_links = []
starting_url = "https://www.normattiva.it/ricerca/elencoPerData"
Starting_links = startingPageLinkToArrayElencoAtti(starting_url)
'''

