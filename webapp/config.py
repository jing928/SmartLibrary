import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    HOST_IP = '127.0.0.1'
    PORT = '5000'

    USER = {
        'username': 'charles',
        'password': 'abc123'
    }

    DATABASE_CONFIG = {
        'HOST': '35.189.0.166',
        'USER': 'root',
        'PASSWORD': 'password',
        'DATABASE': 'SmartLibrary'
    }

    LEND_URL = 'https://datastudio.google.com/embed/reporting/' \
               '1qguKydcbyhQu43qDTeirGt7hBZ3BEwnM/page/VgD'
