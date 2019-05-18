"""
This module provides program entry point for the Reception Pi.
"""

from rp_app.rp_console import RpConsole


class ReceptionPiApp:
    """
    The ReceptionPiApp class provides the method to start the Reception Pi program.
    """

    @staticmethod
    def run():
        """Fires up the Reception Pi console.

        It starts the console UI of the Reception Pi.

        Returns:
            None

        """
        rp_console = RpConsole()
        rp_console.start()


if __name__ == '__main__':
    ReceptionPiApp.run()
