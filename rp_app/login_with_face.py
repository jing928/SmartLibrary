"""
This module has the LoginWithFace class to provide login function with facial recognition
"""

from utils.facial_recognition import FacialRecognition
from utils.file_access import FileAccess
from utils.login_tool import LoginTool
from rp_app.data_access_local import DataAccessLocal


class LoginWithFace:
    """
    The LoginWithFace class provides functions of login with facial recognistion.

    Attributes:
        __server_ip = ip_dict["ip"]: ip address of master pi
        __dao = DataAccessLocal(): data access object to the local database.
        face_rec = FacialRecognition() facial recognition object
    """

    def __init__(self):
        ip_dict = FileAccess.get_ip_config()
        self.__server_ip = ip_dict["ip"]
        self.__dao = DataAccessLocal()
        self.face_rec = FacialRecognition(max_attempts=5)

    def login(self):
        """
        This method will pass username to Master Pi if face matched
        This method will return none if face not matched

        Returns:
            None 
        """
        username = self.face_rec.run()
        if username is None:
            print('No matched face found.\n')
            return

        username_exists = self.__dao.check_if_user_exists(username)
        if not username_exists:
            print("Username doesn't exist...Please register first.\n")
            return

        LoginTool.send_message(username, self.__server_ip)
