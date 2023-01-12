import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from application import config
import os

app=Flask(__name__)

app.config.from_pyfile('config.py')


db = SQLAlchemy(app)
db.init_app(app)



with app.app_context():
    db.create_all()  # Create sql tables for our data models

Migrate(app, db)
from application import models

@app.route('/', methods=['GET'])
def records():
    return 'kakk'


if __name__=='__main__':

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

