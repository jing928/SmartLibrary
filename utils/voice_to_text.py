import speech_recognition as speech
import subprocess


class VoiceToText:

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
        with speech.Microphone(device_index=self.__device_id) as source:
            subprocess.run('clear')
            self.__recognizer.adjust_for_ambient_noise(source)
            print('Please say your search query out loud...\n')
            try:
                self.__audio = self.__recognizer.listen(source, timeout=2)
            except speech.WaitTimeoutError:
                print('Time out! Please try again.')
            finally:
                return self.__audio

    def transcribe(self):
        self.record_audio()
        if self.__audio is None:
            return
        text = None
        try:
            print('Processing...')
            text = self.__recognizer.recognize_google(self.__audio)
            print('You just said "{0}".\n'.format(text))
        except speech.UnknownValueError:
            print('The voice cannot be recognized. Please try again later.')
        except speech.RequestError as error:
            print('Something went wrong. Error: {0}'.format(error))
        finally:
            return text
