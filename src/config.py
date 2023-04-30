# from dotenv import load_dotenv
# import os

# load_dotenv()

# DB_HOST = os.environ.get("DB_HOST")
# DB_PORT = os.environ.get("DB_PORT")
# DB_NAME = os.environ.get("DB_NAME")
# DB_USER = os.environ.get("DB_USER")
# DB_PASS = os.environ.get("DB_PASS")

# SECRET_KEY = os.environ.get("SECRET_AUTH")
# ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
# ALGORITHM = os.environ.get("ALGORITHM")


from dotenv import dotenv_values

config = dotenv_values(".env")

DB_HOST = config.get("DB_HOST")
DB_PORT = config.get("DB_PORT")
DB_NAME = config.get("DB_NAME")
DB_USER = config.get("DB_USER")
DB_PASS = config.get("DB_PASS")

SECRET_KEY = config.get("SECRET_AUTH")
ACCESS_TOKEN_EXPIRE_MINUTES = config.get("ACCESS_TOKEN_EXPIRE_MINUTES")
ALGORITHM = config.get("ALGORITHM")