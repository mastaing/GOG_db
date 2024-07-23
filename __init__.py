from bs4 import BeautifulSoup
import requests
import mysql.connector
from mysql.connector import errorcode

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

def create_database(db_name:str,tables:list,env:list):
    """Création d'une base de donnée mysql
    Args:
        db_name (str): Nom de la base de donnée Mysql à crée
        tables (list): Listes des differentes tables à crée dans la base de donnée
        env (dict): liste des information d'environement MySQL sous la forme :  env={host: host_value, user: user_value, password: password_value})

    Returns: Une data-base mysql
    """
    mydb = mysql.connector.connect(user=env['user'])
    cursor = mydb.cursor()

    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {db_name}")
        exit(1)

    try:
        cursor.execute(f"USE {db_name}")
        print(f"Database {db_name} exists.")
    except mysql.connector.Error as err:
        print(f"Database {db_name} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print(f"Database {db_name} created successfully.")
            mydb.database = db_name
        else:
            print(err)
            exit(1)

    for table_name in tables:
        table_description = tables[table_name]
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

def insert_db(env:dict,db_name:str,dico:dict):
    """insertion des données d'un dictionnaire dans une base de donnée MySQL

    Args:
        env (dict): liste des information d'environement MySQL sous la forme :  env={host: host_value, user: user_value, password: password_value})
        db_name (str): _description_
        dico (dict): _description_
    """
    # Test de connection 
    try:
        mydb = mysql.connector.connect(
        host=env['host'],
        user=env['user'],
        password=env['password'],
        database=db_name
        )
    
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    # Insertion dans la table "games"
    for game,values in dico.items():
        name = game
        base_price = values["base_price"]
        game_price = values["game_price"]
        discount = values["reduction"]
        rating = values["rating"]
        time_to_beat = values["time_to_beat"]
        release_date = values["date"]
        
        
        # verification de presence ou non du jeu dans la table "games"

        sql = "SELECT name FROM games WHERE name = (%s) LIMIT 0, 1"
        val = (name)
        mycursor.execute(sql, (val,))

        try : 
            old_name = mycursor.fetchone()[0]
        except:
            old_name = ""
        mycursor = mydb.cursor(buffered=True)

        if name != old_name:
            sql = "INSERT INTO games (name,base_price,game_price,discount,rating,time_to_beat,release_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (name, base_price, game_price, discount, rating, time_to_beat, release_date)
            mycursor.execute(sql, val)
            mydb.commit()
            print(name , " : ajoutée à la table games")

            #liste des langues du jeux 
            games_languages = values["language"]

            #insertion dans la table "languages"    
            for language in games_languages:
                # recupere la langue du jeux dans la database si elle existe déja
                sql = "SELECT language FROM languages WHERE language = (%s) LIMIT 0, 1"
                val = (language)
                mycursor.execute(sql, (val,))
                try : 
                    old_language = mycursor.fetchone()[0]
                except:
                    old_language = ""
                mycursor = mydb.cursor(buffered=True)

                if old_language != language:
                    sql = "INSERT INTO languages (language) VALUES (%s)"
                    val = (language)
                    mycursor.execute(sql, (val,))
                    mydb.commit()

            #liste des  genre du jeux 
            games_genres = values["genre"]

            
            #insertion dans la table "genres"
            for genre in games_genres:
                # recupere la langue du jeux dans la database si elle existe déja
                sql = "SELECT genre FROM genres WHERE genre = (%s) LIMIT 0, 1"
                val = (genre)
                mycursor.execute(sql, (val,))
                try : 
                    old_genre = mycursor.fetchone()[0]
                except:
                    old_genre = ""
                mycursor = mydb.cursor(buffered=True)

                if old_genre != genre:
                    sql = "INSERT INTO genres (genre) VALUES (%s)"
                    val = (genre)
                    mycursor.execute(sql, (val,))
                    mydb.commit()

            # recupere l'id des jeux
            sql = "SELECT id FROM games WHERE name = (%s)"
            val = (name)
            mycursor.execute(sql, (val,))    
            id_game = mycursor.fetchone()[0]
                
            for language in games_languages:
                # recupere l'id des langues des jeux
                sql = "SELECT id FROM languages WHERE language = (%s)"
                val = (language)
                mycursor.execute(sql, (val,))
                language_game = mycursor.fetchone()[0]

                # Insertion dans la table "games_languages"
                sql = "INSERT INTO games_languages (id_game,language_id) VALUES (%s,%s)"
                val = (id_game,language_game)
                mycursor.execute(sql, val)
                mydb.commit()
                    
            for genre in games_genres:
                # recupere l'id des genres des jeux 
                sql = "SELECT id FROM genres WHERE genre = (%s)"
                val = (genre)
                mycursor.execute(sql, (val,))
                language_game = mycursor.fetchone()[0]

                # Insertion dans la table "games_genres"
                sql = "INSERT INTO games_genres (games_id,genre_id) VALUES (%s,%s)"
                val = (id_game,language_game)
                mycursor.execute(sql, val)
                mydb.commit()
        else:
            #update des jeux déja présent dans la data base
            sql = "UPDATE games SET base_price = %s , game_price = %s , discount = %s , rating = %s , time_to_beat = %s , release_date = %s WHERE name = %s"
            val = (base_price, game_price, discount, rating, time_to_beat, release_date, name)
            mycursor.execute(sql, val)
            mydb.commit()
            print(name , " : actualisé à la table games")
        
    mycursor.close()