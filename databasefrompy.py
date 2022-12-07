import pandas as pd 
import sqlite3

abusive_words = pd.read_csv('abusive.csv')
new_kamus_alay = pd.read_csv('new_kamusalay.csv',encoding='latin-1',names=['slank','KBBI'])

conn = sqlite3.connect('new_database.db')
new_kamus_alay.to_sql('new_kamus_alay',conn, index=False)
abusive_words.to_sql('abusive_words',conn, index=False)



