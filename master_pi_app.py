"""
This module provides program entry point for the Master Pi.
"""

from mp_app.mp_console import MpConsole


class MasterPiApp:
    """
    The MasterPiApp class provides the method to start the Master Pi program.
    """

    @staticmethod
    def run():
        """Fires up the Master Pi console.

        It starts the console UI of the Master Pi.

        Returns:
            None

        """
        mp_console = MpConsole()
        mp_console.start()


if __name__ == '__main__':
    MasterPiApp.run()
