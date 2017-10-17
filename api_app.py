from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from credentials import DBcreds
import flask_restless

api_app = Flask(__name__)
connstring_gppt = 'mysql+mysqlconnector://' + \
                  DBcreds.gppt_db['username'] + ':' + \
                  DBcreds.gppt_db['password'] + '@' + \
                  DBcreds.gppt_db['host'] + ':' + \
                  '3306' + '/' + \
                  DBcreds.gppt_db['database']
api_app.config['SQLALCHEMY_DATABASE_URI'] = connstring_gppt
gppt_db = SQLAlchemy(api_app)
gppt_db.reflect()


class GPPTSubmission(gppt_db.Model):
    __tablename__ = 'gppt_submissions'

manager = flask_restless.APIManager(api_app, flask_sqlalchemy_db=gppt_db)


if __name__ == '__main__':
    api_app.run(debug=True)
    x = 1

