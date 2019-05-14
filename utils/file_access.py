"""
This module provides functions to access JSON files.
"""

import json


class FileAccess:
    """
    FileAccess class provides methods to read JSON config files.
    """

    @staticmethod
    def json_to_dict(path):
        """Reads JSON file and converts it to a Python dictionary.

        Args:
            path: the path of the JSON file.

        Returns:
            dict: a dictionary representation of the JSON file if read in correctly, None otherwise

        """

        try:
            readfile = open(path, 'r')
        except OSError:
            print('Oops...Cannot open the file...')
            return None
        else:
            with readfile:
                content_dict = json.load(readfile)
                return content_dict

    @staticmethod
    def get_db_config():
        """Gets configuration of the cloud database.

        A wrapper method to read database configurations.

        Returns:
            dict: a dictionary representation of the database configurations.
        """
        return FileAccess.json_to_dict('db_config.json')

    @staticmethod
    def get_ip_config():
        """Gets IP address of the server.

        A wrapper method to read IP address of the server.

        Returns:
            dict: a dictionary representation of the database configurations.
        """
        return FileAccess.json_to_dict('ip_config.json')
