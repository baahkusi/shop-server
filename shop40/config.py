from os import getenv
from dotenv import load_dotenv, find_dotenv
import cloudinary
from playhouse.postgres_ext import PostgresqlExtDatabase
load_dotenv(find_dotenv())

# enviromanet variables
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
SENDGRID_API_KEY = getenv("SENDGRID_API_KEY")
TESTING = getenv('TESTING')
CLOUDINARY_API_KEY = getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = getenv('CLOUDINARY_API_SECRET')
CLOUDINARY_NAME = getenv('CLOUDINARY_NAME')
IN_DOCKER = getenv('IN_DOCKER')
DATABASE_URL = getenv('DATABASE_URL')
PLATFORM= getenv('PLATFORM')
FB_ACCESS_TOKEN = getenv('FB_ACCESS_TOKEN')
FB_PAGE_ID=getenv('FB_PAGE_ID')


if PLATFORM != 'heroku':
    host = 'db' if IN_DOCKER=='true' else 'localhost'
    db = PostgresqlExtDatabase(POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                           host=host, port=5432)
else:
    from playhouse.db_url import connect
    db = connect(DATABASE_URL)



