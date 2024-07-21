from bs4 import BeautifulSoup
import requests

def get_max_page(url)-> int: 
    """
        Fonction pour récupérer le nombre maximum de pages sur un site.
    Args:
        url (str): URL du site que l'on va scraper les informations.
    Returns:
        int: Le nombre de pages maximum sur un site.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    element = soup.select_one('#Catalog > div > div.catalog__display-wrapper.catalog__grid-wrapper > div > small-pagination > div > button:nth-child(4) > span')
    return int(element.text)

def get_link(url:str,max_page:int)->list:
    """
        Fonction qui crée une liste des liens des jeux par nombre de pages.

    Args:
        url (str): URL du site que l'on va scraper les informations.
        max_page (int): Le nombre de pages maximum sur un site.

    Returns:
        url_list: Liste des liens de jeux dans la boutique GOG.
    """
    url_list = [] 

    for page_number in range(1, max_page + 1):
        page_url = f"{url}?page={page_number}"
        page = requests.get(page_url)
        soup = BeautifulSoup(page.text,'html.parser')
        for link in soup.find_all('a'):
            if link.get('class') == ['product-tile', 'product-tile--grid'] :
                url_list.append(link.get('href'))
    return url_list



def get_game_info(url:str,balise_class:str):
    """
        Fonction pour scraper des informations depuis un url d'un site avec la classe de la balise rechercher et de la fonction select_one de BeautifulSoup.

    Args:
        url (str):URL du site que l'on va scraper les informations.
        balise_class (str): Chaine de caractère qui représente la classe de la balise html que l'on souhaite récupérer.

    Returns:
        value: Valeur qui représente l'information que l'on voulez récupérer grâce à la classe.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    element = soup.select_one(balise_class)
    return element.text if element else None

def get_game_info_list(url:str,balise_class:str)->list:
    """
        Fonction pour scraper des informations depuis un url d'un site avec la classe de la balise rechercher et de la fonction select_one de BeautifulSoup.

    Args:
        url (str):URL du site que l'on va scraper les informations.
        balise_class (str): Chaine de caractère qui représente la classe de la balise html que l'on souhaite récupérer.

    Returns:
        list: Valeur qui représente l'information que l'on voulez récupérer grâce à la classe sous forme de liste.
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    elements = soup.select(balise_class)
    return [element.get_text(strip=True) for element in elements] if elements else []

def create_games_dictionary(url_list:list,selector_dict:dict)->dict:
    """_summary_

    Args:
        url_list (list): liste d'url des differents jeux 
        balise_class (str): Chaine de caractère qui représente la classe de la balise html que l'on souhaite récupérer.

    Returns:
        dict: dictionnaire du jeux 
    """
    games_dict = {}

    for index in range(len(url_list)) :
        url = url_list[index]
        temp_dict = {}
        
        temp_dict['base_price'] = get_game_info(url, selector_dict['base_price'])
        temp_dict['game_price'] = get_game_info(url, selector_dict['game_price'])

        if temp_dict['base_price'] != temp_dict['game_price'] :
            try:
                temp_dict['reduction'] = round(100 - ((float(temp_dict['game_price']) * 100) / float(temp_dict['base_price'])))
            except:
                temp_dict['reduction'] = None
        else:
            temp_dict['reduction'] = None
        
        temp_dict['rating'] = get_game_info(url_list, selector_dict['rating'])
        temp_dict['genre'] = [get_game_info(url_list, selector_dict['genre_1']), get_game_info(url_list, selector_dict['genre_2']), get_game_info(url_list, selector_dict['genre_3'])]
        temp_dict['language'] = get_game_info_list(url_list, selector_dict['language'])
        temp_dict['time_to_beat'] = get_game_info(url_list, selector_dict['time_to_beat'])
        temp_dict['date'] = get_game_info(url_list, selector_dict['date'])
        games_dict[get_game_info(url_list, selector_dict['title'])] = temp_dict
    return games_dict
