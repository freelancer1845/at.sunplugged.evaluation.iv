'''
Created on 21.07.2017

@author: Jascha Riedel
'''
import numpy as np

def findIsc(data, epsilon  = 0.1):
    '''
    Tries to find the Isc in the given data.
    Parameters:
        data: 2-D Array containing U-I data
        epsilon (optional): defines size of fit range around U = 0
    '''
    
    #epsilon only uses data for fitting where -epsilon < U < epsilon
    startRange = np.where(data[:, 0] > -epsilon)[0][0]
    endRange = np.where(data[:, 0] > epsilon)[0][0]
    
    if endRange <= startRange:
        return findIsc(data, epsilon * 10)
    
    polynom = np.poly1d(np.polyfit(data[startRange:endRange,0], data[startRange:endRange, 1], 1, 1))
    return polynom(0)