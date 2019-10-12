# SHOP 40

An online shop.

## Run

### Using Docker

docker-compose -f docker/development/docker-compose.yml up

### Without Docker

- Set up postgres (check shop40/config.py for config variables)
- pip install -r requirement.txt
- gunicorn -b 0.0.0.0:80 shop40.app:api --reload