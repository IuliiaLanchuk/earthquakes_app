from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('application.config.Config')

db = SQLAlchemy(app)

db.init_app(app)
# with app.app_context():
#     db.create_all()
Migrate(app, db)
@app.route('/', methods =["GET", "POST"])
def index():
    return 'lalhhhhha'

from application import models

if __name__=='__main__':
   app.run(debug=True)