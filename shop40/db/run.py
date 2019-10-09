from ..config import db
from .auth import *


if __name__ == "__main__":
    import sys

    def up():
        print("Creating tables ...")
        db.create_tables([
            Groups, Users, Logins, 
        ])
        print("Successfully created tables ...")

    def down():
        print("Dropping tables ...")
        db.drop_tables([
            Groups, Users, Logins, 
        ])
        print("Successfully dropped tables ...")

    try:
        if sys.argv[1] == "+":
            up()
        elif sys.argv[1] == "-":
            down()
        elif sys.argv[1] == "-+":
            print("Reloading tables ...")
            down()
            up()
            print("Successfully reloaded tables ...")
        else:
            print(f"Could not execute {sys.argv[1]}")
    except Exception as e:
        print(e)
