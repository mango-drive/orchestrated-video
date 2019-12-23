import numpy as np
import pyaudio
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import wave
import queue

from audio_analysis import AudioFile

# TODO Try the call back method of pyaudio
 

class DisplayBuffer:

    def __init__(self, chunk_size, n_chunks):
        self.chunk_size = chunk_size
        self.samples = [0]*chunk_size*n_chunks
    
    def push(self, chunk):
        if len(chunk) == 0:
            del self.samples[:self.chunk_size]
            self.samples.extend([0]*self.chunk_size)
        else: 
            del self.samples[:len(chunk)]
            self.samples.extend(chunk)
    
    def get_samples(self):
        return self.samples

video_frame_rate = 24 # fps
video_frame_interval = 1/24 # milliseconds

wf = wave.open("audio/trap_loop_2.wav", 'rb')

audio_framerate = wf.getframerate()
# TODO find combination of audio framerate and video frame interval that gives an integer
# TODO and a multiple of 2!

CHUNK_SIZE = 3528
chunk_interval = 1000*CHUNK_SIZE // audio_framerate
read_size = CHUNK_SIZE // 2
seconds_displayed = 3
num_chunks = (audio_framerate * seconds_displayed // CHUNK_SIZE)# number of chunks displayed

p = pyaudio.PyAudio()
# TODO input
stream = p.open(format=
                p.get_format_from_width(wf.getsampwidth()),
                rate=wf.getframerate(), 
                output = True, 
                channels = wf.getnchannels(),
                )

display_buff = DisplayBuffer(CHUNK_SIZE, num_chunks)
num_samples = num_chunks * CHUNK_SIZE

fig = plt.figure()
ax = plt.axes(xlim=(0, num_samples-1), ylim=(-200000, 200000))
line, = ax.plot([], [], lw=1)

x = np.linspace(0, num_samples-1, num_samples)

def read_buffer():
    data = wf.readframes(CHUNK_SIZE/2)
    y = np.frombuffer(data, dtype=np.int16)
    yield y

def init():
    line.set_data([], [])
    return line,


def animate(i):
    global x 

    data = wf.readframes(CHUNK_SIZE//2)
    new_chunks = np.frombuffer(data, dtype=np.int16)
    display_buff.push(new_chunks)
    y = display_buff.get_samples()

    line.set_data(x, y)
    return line,

def animate_plot():
    FuncAnimation(fig, animate, init_func = init,  frames = 1000, interval=chunk_interval, blit = True)    
    stream.stop_stream()
    stream.close()
    p.terminate()
    plt.show()


if __name__ == "__main__":
    animate_plot()

