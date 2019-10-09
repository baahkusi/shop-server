# shop-server

Server side application for online shop. Generally designed to fit any shop

### Project Setup

pip install requirements.txt

#### Database Migrations (Postgres Database)

- Set up database variables in shop40.env
- Run "projectdir$ python3 -m shop40.db +" to create all tables
- Run "projectdir$ python3 -m shop40.db -" to drop all tables
- Run "projectdir$ python3 -m shop40.db -+" to drop and create


#### Run Project

gunicorn shop40.app:api --reload
