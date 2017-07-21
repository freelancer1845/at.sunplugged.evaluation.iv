'''
Created on 21.07.2017

@author: Jascha Riedel
'''

import numpy as np

def findRs(data, p = 0.1):
    '''
    Finds the Series Resistance via linear regression by fitting the last 'p' percentage of the U-I data.
    Parameters:
        data: 2-D Array containing U-I data
        p: Percentage of end to be fitted
    
    '''
    
    highestVoltage = np.max(data[:,0])
    
    
    polyCoef = np.polyfit(data[(data[:,0] > highestVoltage * (1-p)) == True, 0], data[(data[:,0] > highestVoltage * (1-p)) == True, 1], 1)
    return polyCoef[0]