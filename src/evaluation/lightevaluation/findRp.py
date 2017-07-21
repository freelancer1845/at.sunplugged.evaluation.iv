'''
Created on 21.07.2017

@author: Jascha Riedel
'''

import numpy as np

def findRp(data, p = 0.2):
    '''
    Finds the Rp via linear Regression by fitting the first 'p' percentage of the U-I data.
    Parameters:
        data: 2-D Array containing U-I data
        p: Percentage of start to be fitted
    '''
    
    lowestVoltage = np.min(data[:,0])
    

    polyCoef = np.polyfit(data[(data[:,0] < lowestVoltage * (1-p)) == True, 0], data[(data[:,0] < lowestVoltage * (1-p)) == True, 1], 1)
    return polyCoef[0]
    
