'''
Created on Jul 1, 2017

@author: Jascha Riedel
'''

import matplotlib.pyplot as matPlot
import numpy as np


class OutputFile:
    
    def __init__(self):
        pass
    
    def addLightPlot(self, voltageCurrentData, keyFeatures):
        
        #fitData = np.poly1d(np.polyfit(voltageCurrentData[:,0], voltageCurrentData[:,1], 3))
        fitData = np.poly1d(np.polyfit(voltageCurrentData[(voltageCurrentData[:,0] > -0.1) & (voltageCurrentData[:,0] < 0.1),0], voltageCurrentData[(voltageCurrentData[:,0] > -0.1) & (voltageCurrentData[:,0] < 0.1),1], 2))
        
        
        print(fitData)
        
        matPlot.plot(voltageCurrentData[:,0], voltageCurrentData[:,1], voltageCurrentData[:,0], fitData(voltageCurrentData[:,0]))
        matPlot.show();
        
        
        
    
    
    def showFile(self):
        pass