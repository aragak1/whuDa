from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config_example import DB_CON_STR

app = Flask(__name__)
app.secret_key = "\x86\xba\xe1\x8f\xfc\x1f\xb6Pb~\xc3}\xe7F\x86\xd3\xf9 |\xa1\xe1\xe6*\x08"

app.config['SQLALCHEMY_DATABASE_URI'] = DB_CON_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

import whuDa.controller.explore
