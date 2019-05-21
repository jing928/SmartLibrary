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
    # DATABASE_CONFIG = {
    # 'HOST': '35.189.0.166'
    # 'USER': 'root'
    # 'PASSWORD': 'password'
    # 'DATABASE': 'SmartLibrary'
    # }