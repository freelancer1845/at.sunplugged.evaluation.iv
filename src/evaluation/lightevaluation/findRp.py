'''
Created on 21.07.2017

@author: Jascha Riedel
'''

import numpy as np

def findRp(data, indexRange = 10):
    '''
    Calculates Rp by fitting (+- indexRange) around I = 0 and
    taking the inverse of the slope.
    Parameters:
        data:        2-D Array with U-I datapoints
        indexRange:  Range around I = 0 of datapoints that will be used for fitting    
    '''
    data = data[data[:,0].argsort()]
    
    firstPositiveCurrent = np.where((data[:, 1] > 0) == True)[0][0]
    fitRange = range(firstPositiveCurrent-indexRange, firstPositiveCurrent+indexRange)
    return 1/np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]
    
