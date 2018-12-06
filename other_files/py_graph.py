from pyqtgraph.Qt import QtGui, QtCore
import numpy as npy
import pyqtgraph as pg
import sys

import pyaudio
import struct
import wave

from scipy.fftpack import fft


class plot_2d(object):
		def __init__(self):
			self.traces = dict()
			self.phase = 0;
			self.t = npy.arange(0, 3.0, 0.01)

			pg.setConfigOptions(antialias=True)
			self.app = QtGui.QApplication(sys.argv)
			self.win = pg.GraphicsWindow(title="Basic plotting examples")
			self.win.resize(1000, 600)
			self.win.setWindowTitle('pyqtgraph example: Plotting')
			self.waveform = self.win.addPlot(title = 'WAVEFORM', row = 1, col = 1)
			self.spectrum = self.win.addPlot(title = 'SPECTRUM', row = 2, col = 1)

			# pyadio stuff
			self.FORMAT = pyaudio.paInt16
			self.CHANNELS = 1
			self.RATE = 44100
			self.CHUNK = 1024*2

			wf = wave.open('C:\\Users\\Nickj\\Desktop\\spectrum_analyzer\\beethoven.wav', 'rb')

			self.p = pyaudio.PyAudio()

			#self.stream = self.p.open(
			#	format= self.FORMAT,
			#	channels=self.CHANNELS,
			#	rate=self.RATE,
			#	input=True,
			#	output=True,
			#	frames_per_buffer=self.CHUNK
			#)

			self.stream = self.p.open(
				format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

			data = wf.readframes(self.CHUNK)
			
			while data != '':
			    self.stream.write(data)
			    data = wf.readframes(self.CHUNK)
			
			self.stream.stop_stream()
			self.stream.close()
			
			self.p.terminate()


			self.x = npy.arange(0, 2*self.CHUNK, 2)
			self.f = npy.linspace(0, self.RATE/2, self.CHUNK/2)



		def start(self):
			if(sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
				QtGui.QApplication.instance().exec_()

		def set_plotdata(self, name, dataset_x, dataset_y):
			if name in self.traces:
				self.traces[name].setData(dataset_x, dataset_y)
			else:
				if name == 'waveform':
					self.traces[name] = self.canvas.plot(pen='y')
					self.waveform.setYRange(0, 255, padding = 0)
					self.waveform.setXRange(0, 2*self.CHUNK, padding = 0.005)

				if name == 'spectrum':
					self.traces[name] = self.canvas.plot(pen='m')				
					self.spectrum.setLogMode(x=True, y=True)
					self.spectrum.setYRange(-4,0,padding = 0)
					self.spectrum.setXRange(
					npy.log10(20),
					np.log10(self.RATE/2,
					padding = .005)
					)

		def update(self):
			wf_data = self.stream.read(self.CHUNK)
			wf_data = struct.unpack(str(2*self.CHUNK) + 'B', wf_data)
			wf_data = npy.array(wf_data, dtype='b')[::2] + 128
			self.set_plotdata(name='waveform', data_x=self.x, data_y=wf_data)
			sp_data = fft(npy.array(wf_data, dtype='int8') - 128)
			sp_data = np.abs(sp_data[0:int(self.CHUNK/2)]) * 2 / (128*self.CHUNK)
			self.set_plotdata(name= 'spectrum', data_x = self.f, data_y=sp_data)

		def animation(self):
			timer = QtCore.QTimer()
			timer.timeout.connect(self.update)
			timer.start(20)
			self.start()

if __name__ ==  '__main__':
	p = plot_2d()
	p.animation()