import os

ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.getenv('DATA_DIR', os.path.join(BASE_DIR, "data"))

DATABASE_NAME = os.getenv('DATABASE_NAME', 'article_db')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.getenv('DATABASE_PORT', 5432)
DATABASE_USER = os.getenv('DATABASE_USER', 'dennis')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', '')

DATABASE_URI = 'postgresql://%s:%s@%s:%s/%s' % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME
)

BASE_VOCAB_SIZE = 1900
RECENT_VOCAB_SIZE = 100

BASE_INDEX_FILE = os.path.join(DATA_DIR, 'base.json')
RECENT_INDEX_FILE = os.path.join(DATA_DIR, 'recent.json')
