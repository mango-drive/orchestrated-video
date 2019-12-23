import time
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import wave
from audio_analysis import AudioFile


audio = AudioFile("audio/trap_loop_2.wav")

samples = audio.samples
sample_rate = audio.get_sampling_rate()
print("Audio file duration: ", len(samples)/sample_rate)
# samples = [1, 0, 0, 0, 0] * 10

n_seconds_displayed = 1
n_samples_displayed = audio.get_sampling_rate() * n_seconds_displayed
# n_samples_displayed = 20

fig = plt.figure()
ax = plt.axes(xlim=(0, n_samples_displayed-1), ylim=(-5, 5))


x = np.linspace(0, n_samples_displayed-1, n_samples_displayed)
line, = ax.plot([], [], lw=1)
        
interval = 40 # ms
chunk = sample_rate * interval // 1000

def init_fig(fig, ax, artists):
    plt.xlim(0, n_samples_displayed-1)
    plt.ylim(-2, 2)
    return artists

def frame_iter(begin, end):
    y = samples[begin, end]

    if end > len(samples):
        pad = [0]*(end - len(samples))
        zero_pad = True
    else:
        zero_pad = False
    

    if zero_pad:
        y = np.concatenate((samples[begin:end], pad), axis = 0)
    else:
        y = samples[begin:end]
    
    yield y

def update_artists(frames, artists, x):
    y = frames
    artists.line.set_data(x, y)



class Anim():
    def __init__(self, fig):
        self.ani = FuncAnimation(fig, self.animate, interval = interval, repeat = False)
        self.stop = False
        self.first = True
        self.t0 = 0

    def animate(self, i):
        if self.first: 
            self.t0 = time.time()
            self.first = False
        if not self.stop:
            begin = i*chunk
            end= begin + n_samples_displayed

            if end > len(samples):
                pad = [0]*(end - len(samples))
                zero_pad = True
            else:
                zero_pad = False
            

            if zero_pad:
                y = np.concatenate((samples[begin:end], pad), axis = 0)
                self.ani.event_source.stop()
                self.stop = True
                t1 = time.time()

                print(t1-self.t0)
            else:
                y = samples[begin:end]
                
            line.set_data(x, y)
        return line, 
    
if __name__ == "__main__":
    anim = Anim(fig)
    plt.show()
