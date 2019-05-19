"""
This module contains the validator class that's used to validate user inputs.
"""

import re


class Validator:
    """
    The Validator class contains static methods to validate various user inputs.
    """

    @staticmethod
    def validate_username(string):
        """Validates user input of the username.

        It compares the user input string with the preset regular expression
        that represents the correct format of the username - minimum of 4
        alphanumeric characters.

        Args:
            string: user input of the username.

        Returns:
            bool: True if the user input matches the regular expression, False otherwise.

        """
        pattern = re.compile(r'^[A-Za-z\d]{4,}$')
        return bool(pattern.match(string))

    @staticmethod
    def validate_fullname(string):
        """Validates user input of the full name of the user.

        It compares the user input string with the preset regular expression
        that represents the correct format of the full name - first name and last name
        with one space in between, only letters are allowed.

        Args:
            string: user input of the full name.

        Returns:
            bool: True if the user input matches the regular expression, False otherwise.

        """
        pattern = re.compile(r'^([A-Za-z])+ ([A-Za-z])+$')
        return bool(pattern.match(string))

    @staticmethod
    def validate_password(string):
        """Validate user input of the password.

        It compares the user input string with the preset regular expression
        that represents the correct format of the password - minimum of 6
        alphanumeric characters, with at least one letter and one number.

        Args:
            string: user input of the password.

        Returns:
            bool: True if the user input matches the regular expression, False otherwise.

        """
        pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$')
        return bool(pattern.match(string))
