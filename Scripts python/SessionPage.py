from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from pyqtgraph import PlotWidget, mkPen
from PyQt6.QtCore import QTimer, QElapsedTimer
from pyqtgraph import ScatterPlotItem, mkBrush, PlotCurveItem, InfiniteLine

import math
import numpy as np
import pandas as pd
import random
import serial
import mmap
import struct

class SessionPage(QMainWindow):
    def __init__(self, paint: bool = False):
        super().__init__()

        self.setWindowTitle("Co-contraction Map")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self.plotter = Plotter(paint=paint)
        
        layout.addWidget(self.plotter)



class Plotter(PlotWidget):
        
    def __init__(self, paint: bool = False):
        super().__init__()

        self.serial_port = serial.Serial('COM9', baudrate=9600)

        self.setMouseEnabled(x=False, y=False)

        # Set the range of the axes
        self.getPlotItem().setLimits(xMin=0, xMax=1.5, yMin=0, yMax=1.5)
        self.plotItem.setRange(xRange=(-1.5, 1.5), yRange=(-1.5, 1.5), padding=0)

        self.setBackground('w')
        self.showGrid(x=False, y=False)
        self.setStyleSheet("border-radius: 0px;")

        # Scatter plot to show the EMG signal point that is being plotted
        self.scatter = ScatterPlotItem(size=10, pen=mkPen(None), brush=mkBrush(0, 255, 0))
        self.addItem(self.scatter)

        # Individual parameters
        self.ue = 0
        self.uf = 0
        self.max_ch1 = 20
        self.max_ch3 = 20
        self.min_ch1 = 2
        self.min_ch3 = 2
        self.mf = 15
        self.me = 0.5
        self.mo = math.tan((math.atan(self.mf)+math.atan(self.me))/2)
        self.mo = 0.7

        # Plotting the lines
        self.flexion_bound = self.plot(pen=mkPen(color='r', width=4))
        self.flexion_bound.setData([0,1/self.mf],[0,1])

        self.extension_bound = self.plot(pen=mkPen(color='b', width=4))
        self.extension_bound.setData([0,1],[0,self.me])

        self.envelope_bound = self.plot(pen=mkPen(color='k', width=4))
        self.envelope_bound.setData([0,1/self.mo],[0,1])

        self.instant_emg = self.plot(pen=mkPen(color="g", width=4)) # Plotting the EMG signal point

        self.timer = QTimer(self) # Timer to update the plot
        if paint:
            self.timer.timeout.connect(self.plot_and_paint_graph)
        else:
            self.timer.timeout.connect(self.plot_graph)
        self.timer.start(20)

        self.elapsed_timer = QElapsedTimer()
        self.elapsed_timer.restart()

    
    def plot_graph(self):
        data = self.serial_port.readline().decode('utf-8').strip(',') # Read data from serial port
        self.uf, self.ue = map(float, data.split(',')) # Parse and split the data into the individual parameters

        # self.uf = random.random()
        # self.ue = random.random()

        # Save data to csv
        with open('data.csv', 'a') as f:
            f.write(f'{self.uf},{self.ue}\n')
        
        self.instant_emg.clear() # Clear the plot
        self.instant_emg.setData([0, self.ue],[0, self.uf]) # Plot the EMG signal point and line to the origin


    def plot_and_paint_graph(self):
        data = self.serial_port.readline().decode('utf-8').strip() # Read data from serial port
        self.uf, self.ue = map(float, data.split(',')) # Parse and split the data into the individual parameters

        # self.uf = random.random()
        # self.ue = random.random()

        # Save data to csv
        with open('data.csv', 'a') as f:
            f.write(f'{self.uf},{self.ue}\n')
        
        self.instant_emg.clear() # Clear the plot
        self.instant_emg.setData([0, self.ue],[0, self.uf]) # Plot the EMG signal point and line to the origin
        self.scatter.addPoints([self.ue], [self.uf], pen=mkPen((0, 0, 0)), brush=mkBrush(0, 255, 0)) # Adds a point at each position that the current point touches

    
    def basic_control(self):
        # Function does not need to be implemented, just uses plot_graph or plot_and_paint_graph
        print()


    def basic_control_with_last_data(self):
        # Plot all the points saved in data.csv, in gray
        data = pd.read_csv('data1.csv', header=None)
        for i in range(len(data)):
            # Plot the last points saved in data1.csv
            self.scatter.addPoints(
                                   [data.iloc[i, 1]], [data.iloc[i, 0]], 
                                   pen=mkPen((0, 0, 0)),
                                   brush=mkBrush((100, 100, 100)) # Gray
                                   )
        

    def angle_control(self, fixed_k: float = 0.5):        
        # Creating the semi-circles on the graph
        theta = np.linspace(-np.pi/2, np.pi/2, 100)
        radius = fixed_k
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        self.semi_circle1 = PlotCurveItem(x, y, pen=mkPen(color=(147, 112, 219), width=4))
        self.semi_circle2 = PlotCurveItem(x*1.5, y*1.5, pen=mkPen(color=(147, 112, 219), width=4))
        self.addItem(self.semi_circle1)
        self.addItem(self.semi_circle2)


    def impedance_control(self, fixed_angle: float = 45):
        angle = fixed_angle

        # Adding the impedance control lines based in the m0 value
        self.line1 = InfiniteLine(pos=(0, 0), angle=angle-10, pen=mkPen(color=(147, 112, 219), width=4))
        self.line2 = InfiniteLine(pos=(0, 0), angle=angle+10, pen=mkPen(color=(147, 112, 219), width=4))
        self.addItem(self.line1)
        self.addItem(self.line2)
    
        self.instant_emg.setData([0, self.ue],[0, self.uf]) # Plot the EMG signal point and line to the origin



def read_from_shared_memory():
    data = [0, 0, 0, 0, 0, 0]
    memory_map_name = "SharedMemoryMap"
    buffer_size = 6 * struct.calcsize('f')  # Tamanho do buffer em bytes para
    with mmap.mmap(-1, buffer_size, memory_map_name) as mmf:
            mmf.read(struct.pack('f'), data)
    print(data)