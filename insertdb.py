


# Connection a la DATABASE

DB_NAME = 'gog_database'

try:
    mydb = mysql.connector.connect(
    host="localhost",
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