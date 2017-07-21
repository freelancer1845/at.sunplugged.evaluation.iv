'''
Created on 21.07.2017

@author: Jascha Riedel
'''

import numpy as np

def findRs(data, indexRange = 10):
    '''
    Calculates Rs by fitting (+- indexRange) around U = 0 and
    taking the inverse of the slope.
    Parameters:
        data:        2-D Array with U-I datapoints
        indexRange:  Range around U = 0 of datapoints that will be used for fitting    
    '''
    data.sort(axis = 0)
    
    firstPositiveVoltage = np.where((data[:, 0] > 0) == True)[0][0]
    fitRange = range(firstPositiveVoltage-indexRange, firstPositiveVoltage+indexRange)

    return 1 / np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]
