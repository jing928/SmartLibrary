import re


class Validator:

    @staticmethod
    def validate_username(string):
        pattern = re.compile(r'^[A-Za-z\d]{4,}$')
        return bool(pattern.match(string))

    @staticmethod
    def validate_fullname(string):
        pattern = re.compile(r'^([A-Za-z])+ ([A-Za-z])+$')
        return bool(pattern.match(string))

    @staticmethod
    def validate_password(string):
        pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')
        return bool(pattern.match(string))
