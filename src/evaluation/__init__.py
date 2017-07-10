'''
Created on Jul 1, 2017

@author: Jascha Riedel
'''

import numpy as np
from scipy import stats
import logging
import matplotlib.pyplot as p
from scipy.interpolate import interp1d
import scipy.optimize

class DarkDataObject:
    '''
        A wrapper class for dark data.
    '''
    

    def createTableData(self):
        self.tableData.append(['Rs', self.Rs])
        self.tableData.append(['Rp', self.Rp])
        
    
    def __init__(self, data, area, texName):
        self.data = data
        self.area = area
        self.texName = texName
        self.Rs = self._findRs(data)
        self.Rp = self._findRp(data)
        self.tableData = []
        self.createTableData()
        
    def _findIsc(self, data, epsilon = 0.1):
        #epsilon only uses data for fitting where -epsilon < U < epsilon
        print(data)
        startRange = np.where(data[:, 0] > -epsilon)[0][0]
        endRange = np.where(data[:, 0] > epsilon)[0][0]
        
        if endRange <= startRange:
            return self._findIsc(data, epsilon * 10)
        
        polynom = np.poly1d(np.polyfit(data[startRange:endRange,0], data[startRange:endRange, 1], 1, 1))
        return polynom(0)
    
    def _findVoc(self, data, epsilon = 0.001):
        #epsilon only uses data for fitting where -epsilon < I < epsilon
        startRange = np.where(((data[:, 1] > -epsilon) == True) & (data[:,0] > 0))[0][0]
        endRange = np.where(((data[:, 1] > epsilon) == True) & (data[:,0] > 0))[0][0]
        if endRange <= startRange:
            return self._findVoc(data, epsilon * 10)
        
        polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                    data[startRange:endRange, 1], 1))
        #p.plot(data[:,0], data[:, 1], data[:,0], polynom(data[:,0]))
        #p.show()
        roots = polynom.r
        if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
            return roots[1]
        else:
            return roots[0]
        
    def _findRp(self, data):
        p = 0.2 # percentage of data start to be fitted
        lowestVoltage = np.min(data[:,0])
        
    
        polyCoef = np.polyfit(data[(data[:,0] < lowestVoltage * (1-p)) == True, 0], data[(data[:,0] < lowestVoltage * (1-p)) == True, 1], 1)
        self.RpC = polyCoef[1]
        return polyCoef[0]
    
    def _findRs(self, data):
        p = 0.1 # percentage of data end to be fitted
        highestVoltage = np.max(data[:,0])
        
        
        polyCoef = np.polyfit(data[(data[:,0] > highestVoltage * (1-p)) == True, 0], data[(data[:,0] > highestVoltage * (1-p)) == True, 1], 1)
        self.RsC = polyCoef[1]
        return polyCoef[0]
    
    def generatePlot(self, axs):
        axs[0].plot(self.data[:,0], self.data[:,1], label='Data', zorder=100)
        axs[0].plot(self.data[:,0], self.Rp * self.data[:,0] + self.RpC)
        axs[0].plot(self.data[:,0], self.Rs * self.data[:,0] + self.RsC)
        axs[0].set_ylim((min(self.data[:,1]) - 0.1 * abs(min(self.data[:,1])) ,max(self.data[:,1]) + 0.1 * abs(max(self.data[:,1]))))
        axs[0].set_xlabel('U')
        axs[0].set_ylabel('I')
        axs[0].set_title(self.texName)
        axs[0].grid()
        axs[0].legend(fontsize=6)
        axs[0].axhline(y=0, color='k')
        axs[0].axvline(x=0, color='k')
        # Create the Table
        
        axs[1].axis('tight')
        axs[1].axis('off')
        table = axs[1].table(cellText=self.tableData,loc='center')
        return axs


class LightDataObject:
    '''
        A wrapper class for light data.
    '''
    def __init__(self, data, area, texName):
        self.data = data
        self.data.sort(axis=0)
        self.area = area
        self.texName = texName
        evaluation = evaluateLightData(data, area)
        self.Voc = evaluation[0]
        self.Isc = evaluation[1]
        self.FF = evaluation[2] * 100
        self.MppX = evaluation[3][0]
        self.Mpp = evaluation[3][1]
        self.jsc = evaluation[4]
        self.Rp = evaluation[5]
        self.Rs = evaluation[6]
        self.Eff = self.Mpp/area/(790/10000)
        self.tableData = []
        self.createTableData()
        
    def createTableData(self):
        self.tableData.append(['Voc', self.Voc])
        self.tableData.append(['Isc', self.Isc])
        self.tableData.append(['FF', self.FF])
        self.tableData.append(['Mpp', self.Mpp])
        self.tableData.append(['jsc', self.jsc])
        self.tableData.append(['Rp', self.Rp])
        self.tableData.append(['Rs', self.Rs])
        self.tableData.append(['Eff', self.Eff])
        
    def generatePlot(self, axs):
        #fig, axs = p.subplots(2, 1, gridspec_kw = {'height_ratios':[2.5, 1]})

        # Do the plot        
        axs[0].plot(self.data[:,0], self.data[:,1], label='Data', zorder=100)
        axs[0].plot(self.data[:,0], self.data[:,0] * self.data[:,1] * -1, label='Power')
        axs[0].plot(self.data[:,0], self.Rp * self.data[:,0] + self.Isc, label='RP')
        axs[0].plot(self.data[:,0],self.Rs * self.data[:,0] - self.Voc * self.Rs, label='RS')
        axs[0].plot(self.Voc, 0, 'x', label='Voc', zorder=200)
        axs[0].plot(0, self.Isc, 'x', label='Isc', zorder=200)
        axs[0].plot(self.MppX, self.Mpp, 'x', label = 'Mpp', zorder=200)
        axs[0].set_ylim((min(self.data[:,1]) - 0.1 * abs(min(self.data[:,1])) ,max(self.data[:,1]) + 0.1 * abs(max(self.data[:,1]))))
        axs[0].set_xlabel('U')
        axs[0].set_ylabel('I')
        axs[0].set_title(self.texName)
        axs[0].grid()
        axs[0].legend(fontsize=6)
        axs[0].axhline(y=0, color='k')
        axs[0].axvline(x=0, color='k')
        # Create the Table
        
        axs[1].axis('tight')
        axs[1].axis('off')
        table = axs[1].table(cellText=self.tableData,loc='center')
        #fig.tight_layout(h_pad=1.4)
        #return fig, axs
        return axs
    
    
def _findIsc(data, epsilon = 0.1):
    # epsilon only uses data for fitting where -epsilon < U < epsilon
    startRange = np.where(data[:, 0] > -epsilon)[0][0]
    endRange = np.where(data[:, 0] > epsilon)[0][0]
    if endRange <= startRange:
        return _findIsc(data, epsilon * 10)
    
    polynom = np.poly1d(np.polyfit(data[startRange:endRange,0], data[startRange:endRange, 1], 1, 1))

    return polynom(0)


def _findVoc(data, epsilon = 0.001):
    # epsilon only uses data for fitting where -epsilon < I < epsilon
    startRange = np.where(((data[:, 1] > -epsilon) == True) & (data[:,0] > 0))[0][0]
    endRange = np.where(((data[:, 1] > epsilon) == True) & (data[:,0] > 0))[0][0]
    
    if endRange <= startRange:
        return _findVoc(data, epsilon * 10)
    
    polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                data[startRange:endRange, 1], 1))
    roots = polynom.r
    if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
        return roots[1]
    else:
        return roots[0]


def _findMpp(data):
    '''
        Finds Mpp by interpolating U*I*-1 in a cubic way.
    '''
    data.sort(axis=0)
    uniqueData = np.array(data)
    for i in range(0, uniqueData[:,0].size):
        if (i < (uniqueData[:,0].size -2)):
            if uniqueData[i,0] == uniqueData[i + 1,0]:
                uniqueData[i,0] = uniqueData[i,0] - 1e-8
    
    iF = interp1d(uniqueData[:,0],uniqueData[:,1] * uniqueData[:,0] * -1, 'cubic')
    x = scipy.optimize.fmin(lambda x: iF(x) * -1, 0, disp=False)
    return np.array([x[0], iF(x)[0]])


def _findRs(data):
    indexRange = 10 # Size of range around U = 0 that will be sampled for linear fit
    
    firstPositiveVoltage = np.where((data[:, 0] > 0) == True)[0][0]
    fitRange = range(firstPositiveVoltage-indexRange, firstPositiveVoltage+indexRange)

    return np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]


def _findRp(data):
    indexRange = 10 # Size of range around U = 0 that will be sampled for linear fit
    
    firstPositiveCurrent = np.where((data[:, 1] > 0) == True)[0][0]
    fitRange = range(firstPositiveCurrent-indexRange, firstPositiveCurrent+indexRange)

    return np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]


def evaluateLightData(data, area):
    '''
        Expects an array where each entry contains a U and I data point.
    '''
    
    Isc = _findIsc(data)
    Voc = _findVoc(data)
    jsc = Isc / area * -1
    MppPoint = _findMpp(data)
    FF = -1 * MppPoint[1] / (Voc * Isc)
    
    Rs = _findRs(data)
    Rp = _findRp(data)
    
   
    return Voc, Isc, FF, MppPoint, jsc , Rs, Rp
   
        
        
        
def evaluateDarkData(data, area):
    Isc = _findIsc(data)
    Voc = _findVoc(data)
    Rs = _findRs(data)
    Rp = _findRp(data)
    return Isc, Voc, Rs, Rp


 
