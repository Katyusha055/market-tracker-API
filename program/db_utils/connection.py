import psycopg
import logging
import os 
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
#this function is for connecting with the database, for now it was built for a local database
#though in theory it should be able to connect to a remote one without problem
load_dotenv()
def connect():
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    if not all([dbname, user, password]):
        raise ValueError("Missing database environment variables")
    try:
        conn = psycopg.connect(dbname=dbname, user=user, password=password)
        logger.info(f'Connected with SQL database {dbname} succesfully')
    except Exception as e:
        raise ConnectionError('Connection failed') from e
    return conn


