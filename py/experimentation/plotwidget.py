
import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QApplication)
import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

class CustomPlot(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data
        print(self.data)
        self.generatePicture()

    def generatePicture(self):
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen('w', width=1/2.))
        for (t, v) in self.data:
            p.drawLine(QtCore.QPointF(t, v-2), QtCore.QPointF(t, v+2))
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        return QtCore.QRectF(self.picture.boundingRect())


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.simpleplot()

    def initUI(self):
        self.guiplot = pg.PlotWidget()
        self.plotItem = self.guiplot.getPlotItem()
        self.plotItem.showAxis('right')
        self.plotItem.hideAxis('left')
        layout = QGridLayout(self)
        layout.addWidget(self.guiplot, 0,0)

    def simpleplot(self):
        data = [
            (1., 10),
            (2., 13),
            (3., 17),
            (4., 14),
            (5., 13),
            (6., 15),
            (7., 11),
            (8., 16)
        ]
        pgcustom = CustomPlot(data)
        self.guiplot.addItem(pgcustom)
        self.plotItem.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())