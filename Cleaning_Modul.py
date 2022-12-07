import pandas as pd 
import re 
import sqlite3


conn = sqlite3.connect('new_database.db',check_same_thread=False)
dfkamusalay = pd.read_sql('SELECT * FROM new_kamus_alay',conn)
dfkamusabusive = pd.read_sql('SELECT * FROM abusive_words',conn)

list_kata_slank = dfkamusalay['slank'].to_list()
list_kata_KBBI = dfkamusalay['KBBI'].to_list()
dict_kata_alay = {slank:KBBI for slank, KBBI in zip(list_kata_slank, list_kata_KBBI )}
dict_abusive = {abusive:'***' for abusive in dfkamusabusive['ABUSIVE'].to_list()}
dict_complete = {**dict_kata_alay,**dict_abusive}

def eliminate_words(text):
    text_split = text.split(' ')
    for word in text_split:
        if word in dict_complete :
            text = re.sub(word,dict_complete[word],text)
    return text

def lowertext(text):
    return text.lower()

def eliminate_unnecessary_char(text):
    text = re.sub('\n',' ', text)
    text = re.sub('rt',' ', text)
    text = re.sub('user',' ', text)
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))',' ',text)
    text = re.sub('  +',' ', text)
    return text

def eliminate_nonaplhanumeric(text):
    text = re.sub('[^0-9a-zA-Z]+', ' ', text)
    text = re.sub('  +',' ', text) 
    return text

def insert_to_database_manualinput(Original_text,Cleaned_text,conn):
    df = pd.Dataframe({'Original_text':[Original_text],'Cleaned_Text':[Cleaned_text]})
    df.to_sql('result',conn, if_exists='append')
    print('sucessfully inserted to database')
    
    
# COMPILE FUNCTIONS
def preprocessing(text):
    text = lowertext(text) # 1
    text = eliminate_unnecessary_char(text) # 2
    text = eliminate_nonaplhanumeric(text) # 3
    text = eliminate_words(text) # 4
    return text


# Untuk Proses File CSV
def processing_csv(input_file):
    first_column = input_file.iloc[:, 0]
    print(first_column)

    for tweet in first_column:
        tweet_clean = preprocessing(tweet)
        query_tabel = "insert into tweet (tweet_kotor,tweet_bersih) values (?, ?)"
        val = (tweet, tweet_clean)
        mycursor.execute(query_tabel, val)
        db.commit()
        print(tweet)



    
    




