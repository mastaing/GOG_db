from fonction import *

DB_NAME = 'gog_database'

TABLES = {}
TABLES['games'] = (
    "CREATE TABLE `games` ("
    " `id` INT NOT NULL AUTO_INCREMENT,"
    " `name` VARCHAR(255) NOT NULL,"
    " `base_price` DECIMAL(5,2) NULL,"
    " `game_price` DECIMAL(5,2) NULL,"
    " `discount` VARCHAR(10) NULL,"
    " `rating` DECIMAL(2,1) NULL,"
    " `time_to_beat` DECIMAL(5,2) NULL,"
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

create_tables(DB_NAME,TABLES)

css_selectors = {
    'base_price' : '.product-actions-price__base-amount',
    'game_price' : '.product-actions-price__final-amount',
    'rating' : '.productcard-rating--inline',
    'genre' : ['.table__row-content > a:nth-child(1)','.table__row-content > a:nth-child(2)','.table__row-content > a:nth-child(3)'],
    'language' : '.details__languages-row--language-name',
    'time_to_beat' : '.howlongtobeat-box__time',
    'title' : '.productcard-basics__title'
    }
                     
insert_data(DB_NAME,create_games_dictionary(get_link("https://www.gog.com/fr/games",1),css_selectors))