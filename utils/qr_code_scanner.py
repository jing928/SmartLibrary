"""
This module provides functionality to scan QR codes
"""

import time
from imutils.video import VideoStream
import imutils
from pyzbar import pyzbar


class QrCodeScanner:
    """
    QrCodeScanner class handles video camera to scan, decode, and save QR codes

    Attributes:
        __video (VideoStream): the video stream service.
        __found (set): a set of scanned QR code data.
    """

    def __init__(self):
        self.__video = VideoStream()
        self.__found = set()

    def scan(self):
        """Scans, decodes, and saves QR code data using the camera

        It will continue scanning QR code until no more QR code is found.

        Returns:
            list: a list of QR code data expressed as string.

        """
        print('Starting video service...')
        self.__video.start()
        print('Warming up the camera...')
        time.sleep(2)
        should_stop = False
        while not should_stop:
            print('Please hold the QR code in front of the camera...\n')
            time.sleep(1)
            found_new = self.__scan_one_frame()
            should_stop = not found_new
        print('Scan complete. Stopping video service...\n')
        self.__video.stop()
        return list(self.__found)

    def __scan_one_frame(self):
        """Scan one frame from the video stream

        It reads one frame and then decode the frame to find QR code.
        If the code hasn't been added to the found set, then added.

        Returns:
            bool: True when found new QR code, False otherwise

        """
        frame = self.__video.read()
        frame = imutils.resize(frame, width=400)
        found_new = False

        qr_codes = pyzbar.decode(frame)
        for qr_code in qr_codes:
            data = qr_code.data.decode('utf-8')
            data_type = qr_code.type

            if data not in self.__found:
                print('Scanned ID: {}, Type: {}\n'.format(data, data_type))
                self.__found.add(data)
                found_new = True
        print('Refreshing...')
        return found_new
