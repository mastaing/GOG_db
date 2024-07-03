import mysql.connector
from mysql.connector import errorcode

# DataBase and Tables 

DB_NAME = 'gog_database'

TABLES = {}
TABLES['games'] = (
    "CREATE TABLE `games` ("
    " `id` INT NOT NULL AUTO_INCREMENT,"
    " `name` VARCHAR(255) NOT NULL,"
    " `base_price` DECIMAL(5,2) NULL,"
    " `game_price` DECIMAL(5,2) NOT NULL,"
    " `discount` VARCHAR(10) NULL,"
    " `rating` DECIMAL(2,1) NOT NULL,"
    " `time_to_beat` DECIMAL(5,2) NOT NULL,"
    " `release_date` DATE NOT NULL,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['genres'] = (
    "CREATE TABLE `genres` ("
    " `id` INT NOT NULL AUTO_INCREMENT,"
    " `genre` VARCHAR(50) NOT NULL,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['languages'] = (
    "CREATE TABLE `languages` ("
    " `id` INT NOT NULL AUTO_INCREMENT,"
    " `language` VARCHAR(50) NOT NULL,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['games_genres'] = (
    "CREATE TABLE `games_genres` ("
    " `games_id` INT NOT NULL,"
    " `genre_id` INT NOT NULL,"
    " INDEX `game_id_idx` (`games_id` ASC),"
    " INDEX `genre_id_idx` (`genre_id` ASC),"
    " PRIMARY KEY (`games_id`, `genre_id`),"
    " CONSTRAINT `game_id`"
    "   FOREIGN KEY (`games_id`)"
    "   REFERENCES `games` (`id`)"
    "   ON DELETE NO ACTION"
    "   ON UPDATE NO ACTION,"
    " CONSTRAINT `genre_id`"
    "   FOREIGN KEY (`genre_id`)"
    "   REFERENCES `genres` (`id`)"
    "   ON DELETE NO ACTION"
    "   ON UPDATE NO ACTION"
    ") ENGINE=InnoDB"
)

TABLES['games_languages'] = (
    "CREATE TABLE `games_languages` ("
    " `id_game` INT NOT NULL,"
    " `language_id` INT NOT NULL,"
    " PRIMARY KEY (`id_game`, `language_id`),"
    " INDEX `language_id_idx` (`language_id` ASC),"
    " CONSTRAINT `id_game`"
    "   FOREIGN KEY (`id_game`)"
    "   REFERENCES `games` (`id`)"
    "   ON DELETE NO ACTION"
    "   ON UPDATE NO ACTION,"
    " CONSTRAINT `language_id`"
    "   FOREIGN KEY (`language_id`)"
    "   REFERENCES `languages` (`id`)"
    "   ON DELETE NO ACTION"
    "   ON UPDATE NO ACTION"
    ") ENGINE=InnoDB"
)



mydb = mysql.connector.connect(user='root')
cursor = mydb.cursor()

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {DB_NAME}")
        exit(1)

# CREATE DATA_BASE and Tables

try:
    cursor.execute(f"USE {DB_NAME}")
    print(f"Database {DB_NAME} exists.")
except mysql.connector.Error as err:
    print(f"Database {DB_NAME} does not exists.")
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
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


        


