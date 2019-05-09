from rp_app.rp_console import RpConsole


class ReceptionPiApp:

    @staticmethod
    def run():
        rp_console = RpConsole()
        rp_console.start()


if __name__ == '__main__':
    ReceptionPiApp.run()
