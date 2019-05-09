import json


class FileAccess:

    @staticmethod
    def json_to_dict(path):
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
        return FileAccess.json_to_dict('db_config.json')
