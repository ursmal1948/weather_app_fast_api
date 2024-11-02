from os import getenv
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = getenv('WEATHER_API_KEY', '')
BASE_URL = getenv('BASE_URL', '')
GEO_BASE_URL = getenv('GEO_BASE_URL', '')

DB_USERNAME = getenv('DB_USERNAME', '')
DB_PORT = getenv('DB_PORT', 3306)
DB_PASSWORD = getenv('DB_PASSWORD', '')
DB_NAME = getenv('DB_NAME', '')
DB_HOST = getenv('DB_HOST', '')
DATABASE_URL = f'mysql+aiomysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
REDIS_PORT = getenv('REDIS_PORT', 6378)
REDIS_HOST = getenv('REDIS_HOST', '')

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
