from mp_app.mp_console import MpConsole

class MasterPiApp:

    @staticmethod
    def run():
        mp_console = MpConsole()
        mp_console.start()


if __name__ == '__main__':
    MasterPiApp.run()
