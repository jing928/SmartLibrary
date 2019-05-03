from rp_app.console import Console


class ReceptionPiApp:

    @staticmethod
    def run():
        console = Console()
        console.start()


if __name__ == '__main__':
    ReceptionPiApp.run()
