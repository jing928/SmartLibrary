"""
This module provides functionality to allow transcribing voice to text.
"""

import subprocess
import speech_recognition as speech


class VoiceToText:
    """
    VoiceToText class provides methods to record audio and transcribe the audio to text
    using Google Speech-to-Text API.

    Attributes:
        MIC_NAME (str): the default microphone of the Master Pi.
        __device_id (int): the index number of the default microphone.
        __recognizer (speech.Recognizer): a speech recognizer instance.
        __audio (AudioData): the recorded audio.
    """

    MIC_NAME = 'Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)'

    def __init__(self):
        device_id = None
        microphone_names = speech.Microphone.list_microphone_names()
        for index, microphone_name in enumerate(microphone_names):
            if microphone_name == VoiceToText.MIC_NAME:
                device_id = index
                break
        self.__device_id = device_id
        self.__recognizer = speech.Recognizer()
        self.__audio = None

    def record_audio(self):
        """Record audio using the default microphone

        It prompts the user to speak and then records and saves the audio.

        Returns:
            None

        """
        with speech.Microphone(device_index=self.__device_id) as source:
            subprocess.run('clear')
            self.__recognizer.adjust_for_ambient_noise(source)
            print('Please say your search query out loud...\n')
            try:
                self.__audio = self.__recognizer.listen(source, timeout=2)
            except speech.WaitTimeoutError:
                print('Time out! Please try again.')
                self.__audio = None

    def transcribe(self):
        """Transcribe the saved audio to text using Google Speech-to-Text API

        It takes the previously saved audio and transcribes it to text.

        Returns:
            str: the transcribed text.
            None: when there is an error.

        """
        self.record_audio()
        if self.__audio is None:
            return None
        try:
            print('Processing...')
            text = self.__recognizer.recognize_google(self.__audio)
            print('You just said "{0}".\n'.format(text))
            return text
        except speech.UnknownValueError:
            print('The voice cannot be recognized. Please try again later.')
            return None
        except speech.RequestError as error:
            print('Something went wrong. Error: {0}'.format(error))
            return None
