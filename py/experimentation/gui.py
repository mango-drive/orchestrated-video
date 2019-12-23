from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QWidget, QGridLayout)

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class WaveformPlot(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        self.x = [1, 2, 3]
        self.y = [4, 5, 6]
        self.plot(self.x, self.y)
        self.clear()
    
class AudioWidget(QWidget):
    def __init__(self):
        super().__init__()
        waveform_plot = WaveformPlot()
        layout = QGridLayout(self)
        layout.addWidget(waveform_plot, 0, 0)

 
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.audioWidget = AudioWidget()
        self.setCentralWidget(self.audioWidget)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()