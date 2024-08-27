from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
from RandomAgent import RandomAgent

def get_max_page(url)-> int: 
    """
        Fonction pour récupérer le nombre maximum de pages sur un site.
    Args:
        url (str): URL du site que l'on va scraper les informations.
    Returns:
        int: Le nombre de pages maximum sur un site.
    """
    page = requests.get(url, RandomAgent())
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
        page = requests.get(page_url, RandomAgent())
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
    page = requests.get(url, RandomAgent())
    soup = BeautifulSoup(page.text,'html.parser')
    element = soup.select_one(balise_class)
    return element.text.strip().replace('\n','') if element else None

def get_game_info_list(url:str,balise_class:str)->list:
    """
        Fonction pour scraper des informations depuis un url d'un site avec la classe de la balise rechercher et de la fonction select de BeautifulSoup.

    Args:
        url (str):URL du site que l'on va scraper les informations.
        balise_class (str): Chaine de caractère qui représente la classe de la balise html que l'on souhaite récupérer.

    Returns:
        list: Valeur qui représente l'information que l'on voulez récupérer grâce à la classe sous forme de liste.
    """
    page = requests.get(url, RandomAgent())
    soup = BeautifulSoup(page.text,'html.parser')
    elements = soup.select(balise_class)
    return [element.get_text(strip=True).replace('\n','') for element in elements] if elements else []

def create_games_dictionary(url_list:list,selector_dict:dict)->dict:
    """_summary_

    Args:
        url_list (list): liste d'url des differents jeux 
        selector_dict(dictionary): dictionnaire de balise de classe
    Returns:
        dict: dictionnaire du jeux 
    """
    games_dict = {}

    for index in range(len(url_list)) :
        url = url_list[index]
        temp_dict = {}

        page = requests.get(url, RandomAgent())
        soup = BeautifulSoup(page.text,'html.parser')

        element = soup.select_one(selector_dict['base_price'])
        temp_dict['base_price'] =  element.text.strip().replace('\n','') if element else None
        #temp_dict['base_price'] = get_game_info(url, selector_dict['base_price'])

        element = soup.select_one(selector_dict['game_price'])
        temp_dict['game_price'] =  element.text.strip().replace('\n','') if element else None
        #temp_dict['game_price'] = get_game_info(url, selector_dict['game_price'])

        if temp_dict['base_price'] != temp_dict['game_price'] :
            try: temp_dict['reduction'] = round(100 - ((float(temp_dict['game_price']) * 100) / float(temp_dict['base_price'])))
            except: temp_dict['reduction'] = None
        else: temp_dict['reduction'] = None

        element = soup.select_one(selector_dict['rating'])
        temp_dict['rating'] = element.text.strip().replace('\n','')[0:3] if element else None
        #temp_dict['rating'] = get_game_info(url, selector_dict['rating'])

        temp_li = []
        element = soup.select_one(selector_dict['genre'][0])
        temp_li.append(element.text.strip().replace('\n','') if element else None)

        element = soup.select_one(selector_dict['genre'][1])
        temp_li.append(element.text.strip().replace('\n','') if element else None)

        element = soup.select_one(selector_dict['genre'][2])
        temp_li.append(element.text.strip().replace('\n','') if element else None)
        temp_dict['genre'] = temp_li
        #temp_dict['genre'] = [get_game_info(url, selector_dict['genre'][0]), get_game_info(url, selector_dict['genre'][1]), get_game_info(url, selector_dict['genre'][2])]
        
        temp_dict['language'] = get_game_info_list(url, selector_dict['language'])[0:3]
        
        element = soup.select_one(selector_dict['time_to_beat'])
        temp_dict['time_to_beat'] =  element.text.strip().replace('\n','').replace(' h','') if element else None
        #temp_dict['time_to_beat'] = get_game_info(url, selector_dict['time_to_beat']).replace(" h",'')
        
        element = soup.select_one(selector_dict['title'])
        games_dict[element.text.strip().replace('\n','') if element else None] = temp_dict
    return games_dict

def create_database(cursor,DB_NAME):
    """fonction pour crée une base de donnée mysql

    Args:
        cursor: curseur my sql
        DB_NAME (str): nom de la base de donnée
    Returns:
        une base de donnée mySQL
    """
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {DB_NAME}")
        exit(1)

def create_tables(DB_NAME:str,TABLES:dict):
    """fonction pour crée une base de donnée mysql

    Args:
        DB_NAME(str): nom de la base de donnée
        TABLES(dictionary): dictionnaire des differentes tables de la base de donnée
    Returns:
        une base de donnée mySQL
    """
    load_dotenv()
    try:
        mydb = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=os.getenv('MYSQL_port'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=DB_NAME
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    cursor = mydb.cursor()

    try:
        cursor.execute(f"USE {DB_NAME}")
        print(f"Database {DB_NAME} exists.")
    except mysql.connector.Error as err:
        print(f"Database {DB_NAME} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor,DB_NAME)
            print(f"Database {DB_NAME} created successfully.")
            mydb.database = DB_NAME
        else:
            print(err)
            exit(1)

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ")
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    mydb.close()

def insert_data(DB_NAME:str,games_dict:dict):
    """fonction pour insére les donnée dans la base de donnée a partir d'un dictionnaire

    Args:
        DB_NAME (str): nom de la base de donnée
        games_dict (dict): dictionnaire des données des differents jeux 
    """
    load_dotenv()
    try:
        mydb = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        port=os.getenv('MYSQL_port'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=DB_NAME
        )

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Mauvais mots de passe ou nom d'utilisateur")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("la base de donnée n'existe pas")
        else:
            print(err)

    mycursor = mydb.cursor(buffered=True)
    for game, values in games_dict.items():
        name = game
        base_price = values["base_price"]
        game_price = values["game_price"]
        discount = values["reduction"]
        rating = values["rating"]
        time_to_beat = values["time_to_beat"]

        # Insertion ou mise à jour dans la table "games"
        sql = """
        INSERT INTO games (name, base_price, game_price, discount, rating, time_to_beat)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        base_price = VALUES(base_price), 
        game_price = VALUES(game_price),
        discount = VALUES(discount), 
        rating = VALUES(rating),
        time_to_beat = VALUES(time_to_beat)
        """
        val = (name, base_price, game_price, discount, rating, time_to_beat)
        mycursor.execute(sql, val)
        mydb.commit()

        print(name, ": inséré ou mis à jour dans la table games")

        # Récupérer l'id du jeu
        sql = "SELECT id FROM games WHERE name = %s"
        mycursor.execute(sql, (name,))
        id_game = mycursor.fetchone()[0]

        # Insérer les langues associées au jeu dans la table "languages"
        for language in values["language"]:
            sql = """
            INSERT INTO languages (language)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE language=language
            """
            mycursor.execute(sql, (language,))
            mydb.commit()

            # Récupérer l'id de la langue
            sql = "SELECT id FROM languages WHERE language = %s"
            mycursor.execute(sql, (language,))
            language_id = mycursor.fetchone()[0]

            # Insérer dans la table de liaison "games_languages"
            sql = """
            INSERT INTO games_languages (id_game, language_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE id_game=id_game, language_id=language_id
            """
            mycursor.execute(sql, (id_game, language_id))
            mydb.commit()

        # Insérer les genres associés au jeu dans la table "genres"
        for genre in values["genre"]:
            sql = """
            INSERT INTO genres (genre)
            VALUES (%s)
            ON DUPLICATE KEY UPDATE genre=genre
            """
            mycursor.execute(sql, (genre,))
            mydb.commit()

            # Récupérer l'id du genre
            sql = "SELECT id FROM genres WHERE genre = %s"
            mycursor.execute(sql, (genre,))
            genre_id = mycursor.fetchone()[0]

            # Insérer dans la table de liaison "games_genres"
            sql = """
            INSERT INTO games_genres (games_id, genre_id)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE games_id=games_id, genre_id=genre_id
            """
            mycursor.execute(sql, (id_game, genre_id))
            mydb.commit()

    mycursor.close()