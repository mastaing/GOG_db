from bs4 import BeautifulSoup
import requests

def get_max_page(url)-> int: 
    """
        Fonction pour recupérer le nombre maximum de page sur un site 
    Args:
        url (str): URL du site que l'on va scraper les informations
    Returns:
        int: Le nombre de pages maximum sur un site
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    element = soup.select_one('#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > div > small-pagination > div > button:nth-child(4) > span')
    return int(element.text)

def get_link(url:str,max_page:int)->list:
    """
        Fonction qui crée une liste des liens des jeux par nombre de page

    Args:
        url (str): URL du site que l'on va scraper les informations
        max_page (int): le nombre de pages maximum sur un site

    Returns:
        list: liste des liens de jeux dans la boutique GOG
    """
    li_game_link = [] 
    for x in range(max_page) :  # crée une liste des liens des jeux par nombre de page
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all('a'):
            if link.get('class') == ['product-tile', 'product-tile--grid'] :
                li_game_link.append(link.get('href'))
    return li_game_link



def get_game_info(url:str,string:str)->str:
    """
        Fonction pour scraper des information depuis un url d'un site, la classe de la balise rechercher et de la fonction select_one de BeautifulSoup

    Args:
        string (str):URL du site que l'on va scraper les informations
        string (str): Chaine de caractere qui represente la class de la balise html que l'on shouaite récupérer

    Returns:
        str: chaine de caractere qui represente l'informaion que l'on voulé récupérer
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    element = soup.select_one(string)
    return element.text

def append_dictionary(dict:str,key:str,value)->dict:
    """_summary_

    Args:
        dict (dict): dictionnaire du jeux
        key (str): clée du dictionnaire
        value (str or int): valeur du dictionnaire

    Returns:
        dict: dictionnaire du jeux 
    """
    dict[key]=value
    return dict
