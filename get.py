from bs4 import BeautifulSoup
from TraitementChaineCara import rreplace
import requests
import mysql.connector
from mysql.connector import errorcode
import string 

print("**Création de la liste des liens de jeux dans la boutique GOG**")

li_game_link = [] #liste des liens de jeux dans la boutique GOG
n_page = 1
for x in range(1) :  # crée une liste des liens des jeux par nombre de page
    url = f"https://www.gog.com/fr/games?page={n_page}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')

    for link in soup.find_all('a'):
        if link.get('class') == ['product-tile', 'product-tile--grid'] :
            li_game_link.append(link.get('href'))
    print("page ",x," chargée")
    n_page += 1 

print("****** Liste crée ******")

print("****** Création du dictionnaire des jeux dans la boutique GOG ******")

games_dict = {} # dictionnaire des jeux  --> Key : nom du jeu / Value : liste de dictionnaire
for link in range(len(li_game_link)) :
#for link in range(1) :
    url = li_game_link[link]
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    game_dict = {}
            # Récupére le Titre du jeu : NOT NULL
    
    element = soup.select_one('.productcard-basics__title')
    print(element.text.strip())

    element = soup.select_one('.product-actions-price__base-amount')
    if element is not None :
        print(element.text)
        base_amount = element.text.strip()

    element = soup.select_one('.product-actions-price__final-amount')
    print(element.text)
    if element is not None :
        final_amount = element.text.strip()

        if base_amount != final_amount :
            reduction = round(100 - ((float(final_amount) * 100) / float(base_amount)))
            print(reduction)

    element = soup.select_one('.productcard-rating--inline')
    print(element.text)

    element = soup.select_one('.table__row-content > a:nth-child(1)')
    print(element.text)

    element = soup.select_one('.table__row-content > a:nth-child(2)')
    print(element.text)

    element = soup.select_one('.table__row-content > a:nth-child(3)')
    print(element.text)    
"""
        # Récupére le Prix de base du jeu : NOT NULL
    game_dict['base_price'] = 0
    for price in soup.find_all('span'):
        if price.get('class') == ['product-actions-price__base-amount', '_price']:
            base_amount = price.string
            game_dict['base_price'] = float(base_amount)

        # Récupére le Prix du jeu : NOT NULL
    game_dict['game_price'] = 0
    for price in soup.find_all('span'):
        if price.get('class') == ['product-actions-price__final-amount', '_price']:
            final_amount = price.string
            game_dict['game_price'] = float(final_amount)

        # Récupére la réduction sur le Prix du jeu 
    if base_amount != final_amount :
        reduction = 100 - ((float(final_amount) * 100) / float(base_amount))
        game_dict['reduction'] = round(reduction)
    else:
        game_dict['reduction'] = 0

        # Récupére la note du jeux
    game_dict['rating'] = 0
    for rating in soup.find_all('div'):
        if rating.get('class') == ['productcard-rating', 'productcard-rating--inline']:
            texte = rating.text[0:3]       
            try :
                float(texte)
                game_dict['rating'] = texte
            except ValueError:
                pass       

        # Récupére les genres du jeux : NOT NULL
    x = 0
    li_genre_game = []
    for genre in soup.find_all('a'):
        if genre.get('class') == ['details__link'] and x < 3:
            if genre.text not in li_genre_game:
                li_genre_game.append(genre.text)
            x += 1
        game_dict['genre'] = li_genre_game

        # Récupére les langues du jeux : NOT NULL
    li_langue_game = []
    for langue in soup.find_all('div'):
        if langue.get('class') == ['details__languages-row--cell', 'details__languages-row--language-name']:
            texte = langue.text.replace("\n","")
            texte = texte.replace(" ","")
            li_langue_game.append(texte)
        game_dict['language'] = li_langue_game


        # Récupére le temps pour finir le jeux
    game_dict['time_to_beat'] = 0
    for howlong in soup.find_all('span'):
        if howlong.get('class') == ['howlongtobeat-box__time'] :
            time = howlong.text.replace("h","")
            try:
                game_dict['time_to_beat'] = float(time.replace(" ",""))
            except:
                game_dict['time_to_beat'] = 0
                

        # Récupére la date de sortie du jeux : 
    x = 0
    game_dict['date'] = ""
    for howlong in soup.find_all('div'):
        if howlong.get('class') == ['details__content', 'table__row-content'] and 'longDate' in howlong.text :
            game_dict['date'] = howlong.text[3:13]
    
    compteur += 1
print("****** Dictionnaire crée ******")
"""
