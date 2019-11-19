from playhouse.migrate import *
from ..config import db
from .shop40 import *
from .auth import *
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
    ],
    [
        migrator.add_index('users', ['name'], unique=True)
    ],
    [
        migrator.drop_column('logins', 'expired')
    ],
    [
        migrator.add_column('users','phone', Users.phone)
    ],
    [
        migrator.drop_not_null('users','name')
    ],
    [
        migrator.add_column('users','logins_failed', Users.logins_failed),
        migrator.add_column('users','login_tries', Users.login_tries)
    ],
    [
        migrator.add_column('items','info', Items.info)
    ],
    [
        migrator.add_column('combinations','is_buyable', Combinations.is_buyable)
    ]
]

if __name__ == "__main__":
    if migrations:
        try:
            print('Loading Migrations ...')
            with db.transaction():
                migrate(*migrations[-1])
            print('Migrations Successfully Completed.')
        except Exception as e:
            print(e)
    else:
        print("No migrations specified ...")
