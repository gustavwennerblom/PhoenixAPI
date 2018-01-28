import logging
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename="PhoenixAPI.log", format=FORMAT, level=logging.DEBUG)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_restless
from credentials import DBcreds
import simplejson as json


def postprocessor(data):
    json.dumps(data, use_decimal=True)

api_app = Flask(__name__)
logging.info("Flask app created")

# Create connection string, using credentials in DBcreds.py in folder credentials
connstring_gppt = 'mysql+mysqlconnector://' + \
                  DBcreds.gppt_db['username'] + ':' + \
                  DBcreds.gppt_db['password'] + '@' + \
                  DBcreds.gppt_db['host'] + ':' + \
                  '3306' + '/' + \
                  DBcreds.gppt_db['database']

# connstring_csi = 'mysql+mysqlconnector://' + \
#                   DBcreds.csi_db['username'] + ':' + \
#                   DBcreds.csi_db['password'] + '@' + \
#                   DBcreds.csi_db['host'] + ':' + \
#                   '3306' + '/' + \
#                   DBcreds.csi_db['database']

# Connect to database and hook SQLAlchemy to it
api_app.config['SQLALCHEMY_DATABASE_URI'] = connstring_gppt      # Default bind referred to as 'None'
# api_app.config['SQLALCHEMY_BINDS'] = {'gppt_db': connstring_gppt}
api_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(api_app)
logging.info("Connection to database established")

# Create metadata from existing database schema
db.reflect(bind=None)
logging.info("GPPT Database metadata reflected")


# Define GPPT submission model
class GPPTSubmission(db.Model):
    __bind_key__ = None
    __tablename__ = 'gppt_submissions'
    logging.info("Model for gppt_submissions created")

# Apply model and instantiate ORM
db.create_all(bind=None)
logging.info("Database models applied")

# Create GPPT API and delimit transferring the actual binary file data
manager = flask_restless.APIManager(api_app, flask_sqlalchemy_db=db)
manager.create_api(GPPTSubmission, methods=['GET'], exclude_columns=['Attachment_Binary'])
logging.info('Endpoint "<base_uri>/api/gppt_submissions" set up')

# Usage:
# Get data on one specific submission from enpoint 'http://localhost:5000/api/gppt_submissions/1'

if __name__ == '__main__':
    api_app.run(debug=False)

