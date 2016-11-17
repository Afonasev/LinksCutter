import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_PATH = os.path.join(BASE_DIR, '../frontend')
SECRET_KEY = os.environ.get('LINKSCUTTER_SECRET_KEY', os.urandom(64))
DATABASE = os.environ.get('LINKSCUTTER_DATABASE', 'db.sqlite3')

MIN_KEY_LENGHT = 6
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
