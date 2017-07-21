'''
Created on 21.07.2017

@author: Jascha Riedel
'''

import numpy as np
import scipy.optimize
from scipy.interpolate import interp1d

def findMpp(data):
    '''
        Finds Mpp by interpolating U*I*-1 in a cubic way.
        Parameters:
            data: 2-D Array containing U-I data
        Returns:
            result: MppU, MppI, Mpp Power
    '''
    data.sort(axis=0)
    uniqueData = np.array(data)
    for i in range(0, uniqueData[:,0].size):
        if (i < (uniqueData[:,0].size -2)):
            if uniqueData[i,0] == uniqueData[i + 1,0]:
                uniqueData[i,0] = uniqueData[i,0] - 1e-8
    
    iF = interp1d(uniqueData[:,0],uniqueData[:,1] * uniqueData[:,0] * -1, 'cubic')
    x = scipy.optimize.fmin(lambda x: iF(x) * -1, 0, disp=False)
    uIInterp = interp1d(uniqueData[:,0], uniqueData[:,1], 'cubic')
    return np.array([x[0], uIInterp(x[0]),  iF(x)[0]])