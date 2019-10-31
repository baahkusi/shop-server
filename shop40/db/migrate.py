from playhouse.migrate import *
from ..config import db
from .shop40 import Users

# initialize migrator
migrator = PostgresqlMigrator(db)

migrations = [
    [
        migrator.add_column('users', 'name', Users.name),
        migrator.add_column('users', 'desc', Users.desc),
    ]
]

if __name__ == "__main__":
    if migrations:
        try:
            print('Loading Migrations ...')
            migrate(*migrations[-1])
            print('Migrations Successfully Completed')
        except Exception as e:
            print(e)
    else:
        print("No migrations specified ...")
