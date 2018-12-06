# -*- coding: utf-8 -*-
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
from numpy import arange, sin, cos, pi
import pyqtgraph as pg
import sys
import time

class Plot2D():
    def __init__(self):
        self.traces = dict()

        #QtGui.QApplication.setGraphicsSystem('raster')
        self.app = QtGui.QApplication([])
        #mw = QtGui.QMainWindow()
        #mw.resize(800,800)

        self.win = pg.GraphicsWindow(title="Basic plotting examples")
        self.win.resize(1000,600)
        self.win.setWindowTitle('pyqtgraph example: Plotting')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.canvas = self.win.addPlot(title="G9")

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def trace(self,name,dataset_x,dataset_y):
        if name in self.traces:
            self.traces[name].setData(dataset_x,dataset_y)
        else:
            self.traces[name] = self.canvas.plot(pen='y')

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    p = Plot2D()
    i = 0
    data = []

    #t = np.arange(.01,6,0.01)
    #s = sin(2 * pi * t + i)
#
#    #print(s)
#    #print(len(s))
#
#    #print("data\n")
# #
# #   #audio_file = open("testfile.txt")
# #   #temp = audio_file.readlines()
# #   #for line in temp:
# #   #    data.append(float(line))
# #   #    #print(float(line))
#
#    #print(data)
    #print(len(data))


    print("entering update\n")

    def update():
        global p, i       
        data = []
 
        audio_file = open('testfile.txt', 'r')
        temp = audio_file.readlines()
        for line in temp:
            data.append(float(line))
            #print(float(line))
        print(str(i) + '\n')
        t = np.arange(.01,6,.01)
        p.trace("data1",t,data)
        audio_file.close()
        i = i + 1
        #if i == 599:
        #    i = 0
        #i += 1

        #global p, i
        #t = np.arange(0,3.0,0.01)
        #s = sin(2 * pi * t + i)
        #c = cos(2 * pi * t + i)
        #p.trace("sin",t,s)
        #p.trace("cos",t,c)
        #i += 0.1

    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(5000)

    p.start()