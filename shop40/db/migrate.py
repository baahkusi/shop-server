from playhouse.migrate import *
from ..config import db
from .shop40 import *
from .auth import *
# initialize migrator
migrator = PostgresqlMigrator(db)

migrations = [
    migrator.add_column('combinations', 'info', Combinations.info),
    migrator.drop_column('likes', 'item_id'),
    migrator.add_column('likes', 'what', Likes.what),
    migrator.add_column('likes', 'pk', Likes.pk),
    migrator.add_column('likes', 'is_liked', Likes.is_liked),
    migrator.drop_not_null('activations','user_id')
]

if __name__ == "__main__":
    if migrations:
        try:
            print('Loading Migrations ...')
            with db.transaction():
                migrate(*migrations)
            print('Migrations Successfully Completed.')
        except Exception as e:
            print(e)
    else:
        print("No migrations specified ...")
