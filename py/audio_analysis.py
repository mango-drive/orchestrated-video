import os
import librosa
import librosa.display
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy import signal

_default_settings = {
    "sr": 44100, # sample rate, Hz
    "filter": {
        "order": 2, # N
        "cutoff": 100, # Hz
        "response": 'lowpass'
    }
}

class Setting:
    def __init__(self, dict = _default_settings):
        self.sr = dict["sr"]
        self.filter = dict["filter"]
    

class AudioFile: 
    def __init__(self, path): 
        # self.x: numpy array representing audio samples
        # self.sr: sample rate of the audio file
        self.x, self.sr = librosa.load(path)
    
    def get_sampling_rate(self):
        return self.sr
    
    def get_duration(self):
        return librosa.get_duration(self.x, self.sr)



class OnsetExtractor:
    def __init__(self, settings = None):
        self.settings = Setting() if settings is None else Setting(settings)

    def extract_onsets(self, audio_file, filter_settings = None):
        # Find estimated locations of onsets in an audio file, using a filter
        # to select a bandwidth in the audio file, and the peak picking algorithm
        # provided by librosa.onset.onset_detect

        # Update the settings to the audio file's sampling rate
        self.settings.sr = audio_file.sr

        # filter the audio
        filter_settings = self.settings.filter if filter_settings is None else filter_settings
        filtered_samples = np.asfortranarray(self._filter(audio_file.x, filter_settings))

        # Detect onset locations, units = seconds
        onset_times = librosa.onset.onset_detect(filtered_samples, units = 'time', backtrack=True)

        return onset_times
    
    def _filter(self, audio_samples, f_settings):
        b, a = signal.butter( f_settings["order"],
                              f_settings["cutoff"],
                              f_settings["response"],
                              fs = self.settings.sr
        )
        
        w, h = signal.freqs(b, a)
        return signal.filtfilt(b, a, audio_samples)

    
 

