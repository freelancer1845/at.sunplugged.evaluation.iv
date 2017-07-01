'''
Created on Jul 01, 2017

@author: Jascha Riedel
'''

from gui.fileIO import readFile
from evaluation import evaluateLightData
from formattedOutput import OutputFile
import os


def testFunction():
    print(os.getcwd())
    data = readFile('../resources/testfiles/20170404/1e/20170404-1e_1-1.txt')
    output = OutputFile()
    output.addLightPlot(data, evaluateLightData(data, 1))