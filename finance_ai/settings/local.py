from .base import *
import environ
from datetime import timedelta

env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / '.env')

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']

# Depending on local needs, you can override database settings or keep the base ones
DATABASES = {
    'default': env.db('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'))
}

# Optional: Disable CORS or add local origins
CORS_ALLOW_ALL_ORIGINS = True
