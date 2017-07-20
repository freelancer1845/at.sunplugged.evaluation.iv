'''
Created on 01.07.2017

@author: Jascha Riedel
'''

import numpy

def readLabViewFile(fileName):
    '''
        Reads a data file and returns a array (Voltage, Current)
    '''
    data = numpy.loadtxt(fileName, skiprows=2);
    return data