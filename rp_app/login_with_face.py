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
        __username (str, None): username stored in encodings.pickle
        __server_ip = ip_dict["ip"]: ip address of master pi
        __dao = DataAccessLocal(): data access object to the local database.
        face_rec = FacialRecognition() facial recognition object
    """

    def __init__(self):
        self.__username = None
        ip_dict = FileAccess.get_ip_config()
        self.__server_ip = ip_dict["ip"]
        self.__dao = DataAccessLocal()
        self.face_rec = FacialRecognition()

    def login(self):
        """
        This method will pass username to Mp if face matched
        This method will return none if face not matched

        Returns:
            None 
        """
        self.__username = self.face_rec.run()
        print(self.__username)
        username_exists = self.__dao.check_if_user_exists(self.__username)
        if not username_exists:
            print("Username doesn't exist...")
            return

        LoginTool.send_message(self.__username, self.__server_ip)
