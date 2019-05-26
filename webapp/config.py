"""
This module provides parameters used in the flask website.
"""
import os


class Config:
    """
    Config class to save env parameters for flask website.

    Attributes:
        SECRET_KEY : used to generate a random key or hard-coded website security key.
        HOST_IP & PORT : flask website ip address and port (both site and api)
        USER : admin login credential
        DATABASE_CONFIG : parameter for cloud database (Google Cloud SQL)
        STAT_URL : URL for Google Data Studio report iframe link
    """
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

    STAT_URL = 'https://datastudio.google.com/embed/reporting/' \
               '1qguKydcbyhQu43qDTeirGt7hBZ3BEwnM/page/VgD'
