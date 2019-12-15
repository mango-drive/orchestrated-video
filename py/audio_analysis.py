import os
import librosa
import librosa.display
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy import signal


class AudioFile: 
    def __init__(self, path): 
        # self.x: numpy array representing audio samples
        # self.sr: sample rate of the audio file
        self.samples, self.sr = librosa.load(path)
    
    def get_sampling_rate(self):
        return self.sr
    
    def get_duration(self):
        return librosa.get_duration(self.x, self.sr)

class AudioProcessingChain:
    chain = []

    def set_next(self, audio_component):
        self.chain.append(audio_component)
        return self
    
    def process(self, samples):
        for component in self.chain:
            samples = component.process(samples)
            
        return samples
            
_default_settings = {
    "sr": 44100, # sample rate, Hz
    "filter": {
        "order": 2, # N
        "cutoff": 100, # Hz
        "response": 'lowpass'
    }
}

class Filter:
    def __init__(self, settings = _default_settings):
        self.settings = settings

    def _filter(self, samples):
        b, a = signal.butter( self.settings["filter"]["order"],
                              self.settings["filter"]["cutoff"],
                              self.settings["filter"]["response"],
                              fs = self.settings["sr"]
        )
        return signal.filtfilt(b, a, samples)

    def process(self, samples):
        return self._filter(samples)


class OnsetExtractor:
    def extract_onsets(self, samples):
        # Find estimated locations of onsets in an audio file, using a filter
        # to select a bandwidth in the audio file, and the peak picking algorithm
        # provided by librosa.onset.onset_detect

        samples = np.asfortranarray(samples)
        # Detect onset locations, units = seconds
        onset_times = librosa.onset.onset_detect(samples, units = 'time', backtrack=True)

        return onset_times
    

    
 

