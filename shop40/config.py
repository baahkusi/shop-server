from os import getenv
from playhouse.postgres_ext import PostgresqlExtDatabase

# enviromanet variables
POSTGRES_DB = getenv("POSTGRES_DB")
POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
SENDGRID_API_KEY = getenv("SENDGRID_API_KEY")
TESTING = getenv('TESTING')

db = PostgresqlExtDatabase(POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                           host='db', port=5432)


