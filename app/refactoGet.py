from bs4 import BeautifulSoup
import requests


print("**Création de la liste des liens de jeux dans la boutique GOG**")

URL = "https://www.gog.com/fr/"
def get_max_page(url:str)->int:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        int: _description_
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    element = soup.select_one('#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > div > small-pagination > div > button:nth-child(4) > span')
    return element.text

    
def get_game_link(url:str, max_page:int)->list:
    """
    Création de la liste des liens de jeux dans la boutique GOG
    
    Args:
        url (str): url du site

    Returns:
        list: list de liens
    """
    li_game_link = [] #liste des liens de jeux dans la boutique GOG
    
    for x in range(max_page) :  # crée une liste des liens des jeux par nombre de page
        page = requests.get(url+str(x))
        soup = BeautifulSoup(page.text,'html.parser')

        for link in soup.find_all('a'):
            if link.get('class') == ['product-tile', 'product-tile--grid'] :
                li_game_link.append(link.get('href'))
    print("page ",x," chargée")
    return li_game_link


max_page = get_max_page('https://www.gog.com/fr/games')
get_game_link(URL+'/games?page=',2)

# import string

# str ="     flflff je csus        "
# print(str)
# print(str.strip()+"a")

    # li_langue_game = []
    # for langue in soup.find_all('div',class_='details__languages-row--cell details__languages-row--language-name'):
    #     li_langue_game.append(langue)
    # game_dict['language'] = li_langue_game

# - Tout mettre dans des fonctions (rien en dehors)
# - Regarder pour le dev modulaire (dans des dossiers (https://github.com/FlorentBch/ygg-lib))
# - Mettre la docstring (extension : autoDocString -> en dessous des fonction tu pas """ et ca va generer automatiquement)
# - Remplacer toute t'es boucles trop large sur une granularité plus fine (for langue in soup.find_all('div',class_='details__languages-row--cell details__languages-row--language-name'):)
# - Remplacer t'es fonctions rreplace par strip
# - variabiliser les variable de bdd en variable d'environnement (DB_USERNAME = localhost) from dotenv import load_dotenv
        # import os
        # # import mysql.connector
        # # from mysql.connector import errorcode

        # # Charger les variables depuis le fichier .env
        # load_dotenv()

        # # Accéder aux variables d'environnement
        # db_username = os.getenv('DB_USERNAME')
        
#  S'interesser au MERGE en SQL pour update facilement la table
# /!\ Apprendre les differents modeles (s'interesser à Merise)
# ++++ Dockeriser l'application et la bdd tout ça dans une image
# API -> FastAPI / Django / Flask
# Integration Power Bi report : https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-embed-secure
# Doc/ jeu git : https://learngitbranching.js.org/?locale=fr_FR

def test(test:int,test2:str)->list:
    """_summary_

    Args:
        test (int): _description_
        test2 (str): _description_

    Returns:
        list: _description_
    """