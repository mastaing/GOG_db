from bs4 import BeautifulSoup
# from TraitementChaineCara import rreplace
import requests
from dotenv import load_dotenv
import os
# import mysql.connector
# from mysql.connector import errorcode

# Charger les variables depuis le fichier .env
load_dotenv()

# Accéder aux variables d'environnement
db_username = os.getenv('DB_USERNAME')

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
compteur = 1
for link in range(len(li_game_link)) :
#for link in range(1) :
    print("Nombre de jeux : ",compteur)
    url = li_game_link[link]
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    game_dict = {}

            # Récupére le Titre du jeu : NOT NULL
    for title in soup.find_all('h1'):
        titre = title.text
        titre = titre.replace("\n","")
        # titre = rreplace(titre, " ", "")
        titre = titre.replace(" ","",8)
        games_dict[titre] = game_dict

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

    #     # Récupére les langues du jeux : NOT NULL
    # li_langue_game = []
    # for langue in soup.find_all('div'):
    #     if langue.get('class') == ['details__languages-row--cell', 'details__languages-row--language-name']:
    #         texte = langue.text.replace("\n","")
    #         texte = texte.replace(" ","")
    #         li_langue_game.append(texte)
    #     game_dict['language'] = li_langue_game
        
    li_langue_game = []
    for langue in soup.find_all('div',class_='details__languages-row--cell details__languages-row--language-name'):
        li_langue_game.append(langue)
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

# Connection a la DATABASE

DB_NAME = 'gog_database'

try:
    mydb = mysql.connector.connect(
    host=db_username,
    user="root",
    password="",
    database=DB_NAME
    )

except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

mycursor = mydb.cursor()

genre_list = []
languages_list = []

for game,values in games_dict.items():
    name = game
    base_price = values["base_price"]
    game_price = values["game_price"]
    discount = values["reduction"]
    rating = values["rating"]
    time_to_beat = values["time_to_beat"]
    release_date = values["date"]

    # Insertion dans la table "games"
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
mydb.close()
