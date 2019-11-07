from playhouse.migrate import *
from ..config import db
from .shop40 import Users

# initialize migrator
migrator = PostgresqlMigrator(db)

migrations = [
    [
        migrator.drop_column('users','phone'),
        migrator.drop_column('users','desc'),
        migrator.drop_column('users','phone'),
        migrator.drop_column('users','desc'),
        migrator.add_column('users', 'info', Users.info),
    ],
    [
        migrator.drop_column('users','info'),
        migrator.add_column('users', 'info', Users.info)
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
