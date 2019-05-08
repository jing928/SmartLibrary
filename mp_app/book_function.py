from mp_app.data_access_cloud import DataAccessCloud


class BookFunction:

    def __init__(self, username):
        self.__username = username
        self.__dao = DataAccessCloud()
        user_id = self.__dao.get_user_id(username)
        if user_id is None:
            raise Exception('Username does not exist.')
        self.__user_id = user_id
