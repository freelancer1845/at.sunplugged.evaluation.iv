'''
Created on 19.07.2017

@author: jasch
'''

import numpy as np
from scipy.interpolate import interp1d
import scipy.optimize

class LightEvaluation():
    '''
    Utility Class containing all functions needed to calculate 'LightData'
    
    Methods:
        findVoc:
            data: 2-D Array containing U-I data
            epsilon (optional): defines size of linear fit around I = 0
        findIsc
            data: 2-D Array containing U-I data
            epsilon (optional): defines size
    '''


    def __init__(self):
        '''
        Should never be called
        '''
      
      
    @staticmethod
    def findVoc(data, epsilon = 0.001):
        '''
        Tries to find the Voc in the given data.
        Parameters:
            data: 2-D Array containing U-I data
            epsilon (optional): defines size of linear fit around I = 0
        '''
        
        #epsilon only uses data for fitting where -epsilon < I < epsilon
        startRange = np.where(((data[:, 1] > -epsilon) == True) & (data[:,0] > 0))[0][0]
        endRange = np.where(((data[:, 1] > epsilon) == True) & (data[:,0] > 0))[0][0]
        if endRange <= startRange:
            return LightEvaluation.findVoc(data, epsilon * 10)
        
        polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                    data[startRange:endRange, 1], 1))
        #p.plot(data[:,0], data[:, 1], data[:,0], polynom(data[:,0]))
        #p.show()
        roots = polynom.r
        if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
            return roots[1]
        else:
            return roots[0]
        
        
        
    @staticmethod
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
            return LightEvaluation.findIsc(data, epsilon * 10)
        
        polynom = np.poly1d(np.polyfit(data[startRange:endRange,0], data[startRange:endRange, 1], 1, 1))
        return polynom(0)



    @staticmethod
    def findMpp(self, data):
        '''
            Finds Mpp by interpolating U*I*-1 in a cubic way.
            Parameters:
                data: 2-D Array containing U-I data
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

    @staticmethod
    def findRp(self, data, p = 0.2):
        '''
        Finds the Rp via linear Regression by fitting the first 'p' percentage of the U-I data.
        Parameters:
            data: 2-D Array containing U-I data
            p: Percentage of start to be fitted
        '''
        
        lowestVoltage = np.min(data[:,0])
        
    
        polyCoef = np.polyfit(data[(data[:,0] < lowestVoltage * (1-p)) == True, 0], data[(data[:,0] < lowestVoltage * (1-p)) == True, 1], 1)
        self.RpC = polyCoef[1]
        return polyCoef[0]
    
    @staticmethod
    def findRs(self, data, p = 0.1):
        '''
        Finds the Series Resistance via linear regression by fitting the last 'p' percentage of the U-I data.
        Parameters:
            data: 2-D Array containing U-I data
            p: Percentage of end to be fitted
        
        '''
        
        highestVoltage = np.max(data[:,0])
        
        
        polyCoef = np.polyfit(data[(data[:,0] > highestVoltage * (1-p)) == True, 0], data[(data[:,0] > highestVoltage * (1-p)) == True, 1], 1)
        self.RsC = polyCoef[1]
        return polyCoef[0]
    
    
    