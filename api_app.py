import logging
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename="PhoenixAPI.log", format=FORMAT, level=logging.DEBUG)

from flask import Flask
import flask_restless
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from credentials import DBcreds
import simplejson as json


def postprocessor(data):
    json.dumps(data, use_decimal=True)

api_app = Flask(__name__)
logging.info("Flask app created")

# Create connection string #1, using credentials in DBcreds.py in folder credentials
connstring_gppt = 'mysql+mysqlconnector://' + \
                  DBcreds.gppt_db['username'] + ':' + \
                  DBcreds.gppt_db['password'] + '@' + \
                  DBcreds.gppt_db['host'] + ':' + \
                  '3306' + '/' + \
                  DBcreds.gppt_db['database']

# Create connection string #1, using credentials in DBcreds.py in folder credentials
connstring_css = 'mysql+mysqlconnector://' + \
                  DBcreds.csi_db['username'] + ':' + \
                  DBcreds.csi_db['password'] + '@' + \
                  DBcreds.csi_db['host'] + ':' + \
                  '3306' + '/' + \
                  DBcreds.csi_db['database']

# Connect to database #1 and hook SQLAlchemy to it
Base_gppt = declarative_base()
engine = create_engine(connstring_gppt)
logging.info("Connection to database established")
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
mysession = scoped_session(Session)
metadata = MetaData(bind=engine)



# Create metadata from existing database schema
# engine.reflect()
# logging.info("Database metadata reflected")

# Define model
class GPPTSubmission(Base_gppt):
    __tablename__ = 'gppt_submissions'
    __table__ = Table('gppt_submissions', metadata, autoload=True)
    logging.info("Model for gppt_submissions created")

class CSATProject(Base_gppt):
    __tablename__ = 'projects'



# Apply model and instantiate ORM
logging.info("Database models applied")

# Create APIs and delimit transferring the actual binary file data
manager = flask_restless.APIManager(api_app, session=mysession)
manager.create_api(GPPTSubmission, methods=['GET'], exclude_columns=['Attachment_Binary'])
logging.info('Endpoint "<base_uri>/api/gppt_submissions" set up')

# Usage:
# Get data on one specific submission from enpoint 'http://localhost:5000/api/gppt_submissions/1'

if __name__ == '__main__':
    api_app.run(debug=False)

