import re
import pandas as pd
import sqlite3
from Cleaning_Modul import preprocessing,processing_csv
from flask import Flask, jsonify
from pathlib import Path
db_path = Path(__file__).parent/'new_database.db'
conn = sqlite3.connect('new_database.db',check_same_thread=False)



app = Flask(__name__)

from flask import request
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from


app.json_encoder = LazyJSONEncoder
swagger_template = dict(
    info = {
        'title': LazyString(lambda: 'API For Cleaning Abusive and Slank Languange in Your Text'),
        'version': LazyString(lambda: '1.0.0'),
        'description': LazyString(lambda: 'Made by Jan Michael Edward Tinsay')
    },
    host = LazyString(lambda: request.host)
)
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'docs',
            "route": '/docs.json'
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}
swagger = Swagger(app, template=swagger_template,config=swagger_config)

@swag_from("docs/hello_world.yml", methods=['GET'])
@app.route('/Welcoming-users', methods=['GET'])
def hello_world():
    json_response = {
        'status_code': 200,
        'description': "This API works!",
        'Welcome': "Hello Binar"
    }

    response_data = jsonify(json_response)
    return response_data


@swag_from("docs/text_processing.yml", methods=['POST'])
@app.route('/text-processing', methods=['POST'])
def text_processing_input():

    text = request.form.get('text')
    cleaned = preprocessing(text)
    dfclean = pd.DataFrame({'raw_text':[text],'cleaned text':[cleaned]})
    dfclean.to_sql('result_table',conn,index=False, if_exists='append')
    json_response = {
        'status_code': 200,
        'description': "This is your cleaned text",
        'Initial_data': text,
        'cleansed_data': cleaned
    }

    response_data = jsonify(json_response)
    return response_data

@swag_from("docs/Upload_csv.yml", methods=['POST'])
@app.route('/Upload-csv', methods=['POST'])
def text_processing_upload():

    file = request.files.get('file')
    df = pd.read_csv(file,encoding="latin-1",on_bad_lines='skip',low_memory=False,sep=';')
    clean_string= []
    raw_string=[]
    for row in df['Tweet'].to_list():
        raw_string.append(row)
        clean = preprocessing(row)
        clean_string.append(clean)
    dfaclean = pd.DataFrame({'raw_text':raw_string,'cleaned text':clean_string})
    dfaclean.to_sql('result_table',conn,index=False, if_exists='append')
    
    response_data = jsonify(dfaclean.T.to_dict())
    return response_data

    

if __name__ == '__main__':
    app.run(debug=True)
