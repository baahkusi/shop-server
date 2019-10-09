from playhouse.migrate import *
from ..config import db

# initialize migrator
migrator = PostgresqlMigrator(db)

migrations = [
    
]

if __name__ == "__main__":
    if not migrations:
        migrate(*migrations[-1])
    else:
        print("No migrations specified ...")
