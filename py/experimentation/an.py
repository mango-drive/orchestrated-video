
import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import wave
from audio_analysis import AudioFile
from collections import namedtuple
from functools import partial


audio = AudioFile("audio/trap_loop_2.wav")

samples = audio.samples
sample_rate = audio.get_sampling_rate()
print("Audio file duration: ", len(samples)/sample_rate)
# samples = [1, 0, 0, 0, 0] * 10

n_seconds_displayed = 1
n_samples_displayed = audio.get_sampling_rate() * n_seconds_displayed
# n_samples_displayed = 20

x = np.linspace(0, n_samples_displayed-1, n_samples_displayed)
        
interval = 40 # ms
chunk = sample_rate * interval // 1000

def init_fig(fig, ax, artists):
    plt.xlim(0, n_samples_displayed-1)
    plt.ylim(-2, 2)
    return artists

def frame_iter():
    for i in range(len(samples)/chunk):
        begin = i*chunk
        end = begin + n_samples_displayed
        if end > len(samples):
            pad = [0]*(end - len(samples))
            y = np.concatenate((samples[begin:end], pad), axis = 0)
        else:
            y = samples[begin:end]
        yield y

def update_artists(frames, artists, x):
    y = frames
    artists.line.set_data(x, y)

Artists = namedtuple("Artists", ("line"))
artists = Artists(
    plt.plot([], [], animated=True)[0]
)

init = partial(init_fig, fig=fig, ax=ax, artists = artists)
step = partial(frame_iter)
