from flask import Flask
import os
import yaml

from datetime import timedelta


with open('../keys.yml', 'r') as file:
    keys = yaml.safe_load(file)

Blockchain_Keys                         = keys['Blockchain_Keys']
Chimere_Aws_database                    = keys['Chimere_Aws_database']
Smart_Contract_Address                  = keys['Smart_Contract_Address']

with open('../database_structure.yml', 'r') as file:
    db_structure = yaml.safe_load(file)


app                                     = Flask(__name__)

SECRET_KEY                              = os.urandom(32)
app.config['SECRET_KEY']                = SECRET_KEY
app.config['Blockchain_Keys']           = Blockchain_Keys
app.config['Chimere_Aws_database']      = Chimere_Aws_database
app.config['Smart_Contract_Address']    = Smart_Contract_Address
app.config['DB_Structure']              = db_structure


from Chimere_Pay import routes