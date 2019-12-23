import numpy as np
import pyaudio
import wave
import time
import sys
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QWidget, QGridLayout)

MILLI_to_SEC = 0.001

class DisplayBuffer:

    def __init__(self, chunk_n, chunk_len):

        self.chunk_len = chunk_len
        self.samples = [0]*self.chunk_len*chunk_n
    
    def push(self, chunk):
        # Delete samples at from to make space for the chunk at the back
        del self.samples[:self.chunk_len]

        if len(chunk) == 0:
            chunk = np.int16(chunk)
        if len(chunk) < self.chunk_len:
            pad = [np.int16(0)]*(self.chunk_len - len(chunk))
            chunk = np.concatenate((chunk, pad), axis = 0)
        self.samples.extend(chunk)
    
    def get_samples(self):
        return self.samples
    
    def __str__(self):
        return str(self.samples)
        

class AudioStream:
    stream = None
    def __init__(self, audio_path):
        self.wf = wave.open(audio_path, 'rb')

    def read(self, chunk_len):
        wf_data = self.wf.readframes(chunk_len) 
        wf_data = np.frombuffer(wf_data, dtype = np.int16)[::2]
        return wf_data
    
    def get_sampling_rate(self):
        return self.wf.getframerate()

class WaveformPlot(pg.PlotWidget):
    def __init__(self, audio_path):
        super().__init__()
        self.update_interval = 40 # ms

        self.stream = AudioStream(audio_path)
        self.audio_rate = self.stream.get_sampling_rate()

        self.chunk_len = int(self.update_interval * MILLI_to_SEC * self.audio_rate)
        self.chunk_n = 40
        self.tot_samples = self.chunk_len * self.chunk_n
        self.display_buffer = DisplayBuffer(self.chunk_n, self.chunk_len)

        wf_xlabels = [(0, '0'), (2048, '2048')]
        wf_xaxis = pg.AxisItem(orientation='bottom')
        wf_xaxis.setTicks([wf_xlabels])

        wf_ylabels = [(0, '0'), (22000, '22000'), (44000, '44000')]
        wf_yaxis = pg.AxisItem(orientation='left')
        wf_yaxis.setTicks([wf_ylabels])

        self.x = np.arange(0, self.tot_samples, 1)
        self.timer = QtCore.QTimer()
        
    def update(self):
        data = self.stream.read(self.chunk_len)
        self.display_buffer.push(data)
        
        self.setYRange(-44000, 44000, padding=0)
        self.setXRange(0, self.tot_samples, padding=0.005)

        self.clear()
        self.plot(self.x, 
                            self.display_buffer.get_samples(),
                            pen='c')

    def animation(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(self.update_interval)


 
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.audioWidget = WaveformPlot("audio/trap_loop_2.wav")
        self.setCentralWidget(self.audioWidget)
        self.audioWidget.animation()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


