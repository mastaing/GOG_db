import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='gog_database'
    )

df_games = pd.read_sql_query("SELECT * from games", mydb)
df_genres = pd.read_sql_query("SELECT * from genres", mydb)
df_languages = pd.read_sql_query("SELECT * from languages", mydb)
df_games_genres = pd.read_sql_query("SELECT * from games_genres", mydb)
df_games_languages = pd.read_sql_query("SELECT * from games_languages", mydb)
print(df_games)
print(df_genres)
print(df_languages)
print(df_games_genres)
print(df_games_languages)
mydb.close()