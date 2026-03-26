from .base import *
import environ
import os

env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR / '.env')

DEBUG = False

# Production allowed hosts (read from .env, comma-separated ideally)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['your-production-domain.com'])

DATABASES = {
    'default': env.db('DATABASE_URL')
}

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CORS and CSRF configurations for production
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=[])
