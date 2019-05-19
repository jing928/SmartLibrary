from utils.facial_rec import FacialRecognition
from utils.file_access import FileAccess
from utils.login_tool import LoginTool
from rp_app.data_access_local import DataAccessLocal


class LoginWithFace:

    def __init__(self):
        self.__username = None
        ip_dict = FileAccess.get_ip_config()
        self.__server_ip = ip_dict["ip"]
        self.__dao = DataAccessLocal()
        self.face_rec = FacialRecognition()

    def login(self):
        self.__username = self.face_rec.get_username()
        print(self.__username)
        username_exists = self.__dao.check_if_user_exists(self.__username)
        if not username_exists:
            print("Username doesn't exist...")
            return

        LoginTool.send_message(self.__username, self.__server_ip)
