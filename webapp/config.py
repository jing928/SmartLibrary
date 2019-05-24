import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # HOST_IP = '10.132.54.164'
    HOST_IP = '127.0.0.1'
    # HOST_IP = '192.168.1.7'
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

    # LEND_URL = 'https://datastudio.google.com/embed/reporting/1ni-4ZoFqrTgkxDg1SVKgw7r2gUkvQIgh/page/yYBq'    # v0
    # LEND_URL = 'https://datastudio.google.com/embed/reporting/14OJZfPlkPp7RNTERAnLz7PnCLPYmvCn2/page/9SZq'	# v1
    RETURN_URL = 'https://datastudio.google.com/embed/reporting/1xNEctzAzy9-LU1GsN1QKZp7UL6q5Av6c/page/vHPq'
    # RETURN_URL = 'https://datastudio.google.com/open/1xNEctzAzy9-LU1GsN1QKZp7UL6q5Av6c'
    LEND_URL = 'https://datastudio.google.com/embed/reporting/1qguKydcbyhQu43qDTeirGt7hBZ3BEwnM/page/VgD'
