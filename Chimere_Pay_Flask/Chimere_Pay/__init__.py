from flask import Flask
import os
import psycopg2.pool

from datetime import timedelta





app                                     = Flask(__name__)

SECRET_KEY                              = os.urandom(32)
app.config['SECRET_KEY']                = SECRET_KEY





# app.config["Connection Pool"]           = pool



from Chimere_Pay import routes