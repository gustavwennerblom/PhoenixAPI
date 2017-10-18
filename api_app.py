from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless
from credentials import DBcreds
import simplejson as json


def postprocessor(data):
    json.dumps(data, use_decimal=True)

api_app = Flask(__name__)

# Create connection string, using credentials in DBcreds.py in folder credentials
connstring_gppt = 'mysql+mysqlconnector://' + \
                  DBcreds.gppt_db['username'] + ':' + \
                  DBcreds.gppt_db['password'] + '@' + \
                  DBcreds.gppt_db['host'] + ':' + \
                  '3306' + '/' + \
                  DBcreds.gppt_db['database']

# Connect to database and hook SQLAlchemy to it
api_app.config['SQLALCHEMY_DATABASE_URI'] = connstring_gppt
api_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
gppt_db = SQLAlchemy(api_app)

# Create metadata from existing database schema
gppt_db.reflect()

# Define model
class GPPTSubmission(gppt_db.Model):
    __tablename__ = 'gppt_submissions'

# Apply model and instantiate ORM
gppt_db.create_all()

# Create APIs and delimit transferring the actual binary file data
manager = flask_restless.APIManager(api_app, flask_sqlalchemy_db=gppt_db)
manager.create_api(GPPTSubmission, methods=['GET'], exclude_columns=['Attachment_Binary'])


# Usage:
# Get data on one specific submission from enpoint 'http://localhost:5000/api/gppt_submissions/1'

if __name__ == '__main__':
    api_app.run(debug=True)

