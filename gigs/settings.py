import os 
TEMPLATES_AUTO_RELOAD = True

DATABASE_URL = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')