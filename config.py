from dotenv import load_dotenv
import os

load_dotenv()  # loading enviroment variables

class Config:   
    DEBUG = False
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DB = os.environ.get("MYSQL_DB")

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get("SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "development"
