from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

db.init_app(app)

@app.route('/', methods =["GET", "POST"])
def index():
    return 'lalhhhhha'


if __name__=='__main__':
   app.run(debug=True)