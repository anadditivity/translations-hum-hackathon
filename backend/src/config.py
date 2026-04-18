import os

DB_USER:str = os.getenv('POSTGRES_USER', 'env var username not found')
DB_PASSWORD:str = os.getenv('POSTGRES_PASSWORD', 'env var password not found')
