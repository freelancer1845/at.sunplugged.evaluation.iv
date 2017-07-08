'''
Created on Jul 1, 2017

@author: Jascha Riedel
'''

import numpy as np
from scipy import stats
import logging
import matplotlib.pyplot as p


class LightDataObject:
    '''
        A wrapper class for light data.
    '''

    
    def createTableData(self):
        self.tableData.append(['Voc', self.Voc])
        self.tableData.append(['Isc', self.Isc])
        self.tableData.append(['FF', self.FF])
        self.tableData.append(['Mpp', self.Mpp])
        self.tableData.append(['jsc', self.jsc])
        self.tableData.append(['Rp', self.Rp])
        self.tableData.append(['Rs', self.Rs])
        self.tableData.append(['Eff', self.Eff])
    
    def __init__(self, data, area, texName):
        self.data = data
        self.area = area
        self.texName = texName
        evaluation = evaluateLightData(data, area)
        self.Voc = evaluation[0]
        self.Isc = evaluation[1]
        self.FF = evaluation[2]
        self.MppX = evaluation[3][0]
        self.Mpp = evaluation[3][1]
        self.jsc = evaluation[4]
        self.Rp = evaluation[5]
        self.Rs = evaluation[6]
        self.Eff = self.Mpp/area/(790/10000)
        self.tableData = []
        self.createTableData()
        
    def generatePlot(self, axs):
        #fig, axs = p.subplots(2, 1, gridspec_kw = {'height_ratios':[2.5, 1]})

        # Do the plot        
        axs[0].plot(self.data[:,0], self.data[:,1], label='Data')
        axs[0].plot(self.data[:,0], self.data[:,0] * self.data[:,1] * -1, label='Power')
        axs[0].plot(self.data[:,0], self.Rp * self.data[:,0] + self.Isc, label='RP')
        axs[0].plot(self.data[:,0],self.Rs * self.data[:,0] - self.Voc * self.Rs, label='RS')
        axs[0].plot(self.Voc, 0, 'x', label='Voc')
        axs[0].plot(0, self.Isc, 'x', label='Isc')
        axs[0].plot(self.MppX, self.Mpp, 'x', label = 'Mpp')
        axs[0].set_ylim((min(self.data[:,1]),max(self.data[:,1])))
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
    
    
def _findIsc(data):
    epsilon = 0.1  # only uses data for fitting where -epsilon < U < epsilon
    
    polynom = np.poly1d(np.polyfit(data[(data[:, 0] > -epsilon) & (data[:, 0] < epsilon), 0],
                data[(data[:, 0] > -epsilon) & (data[:, 0] < epsilon), 1], 2))
    return polynom(0)


def _findVoc(data):
    epsilon = 0.001  # only uses data for fitting where -epsilon < I < epsilon
    startRange = np.where((data[:, 1] > -epsilon) == True)[0][0]
    endRange = np.where((data[:, 1] > epsilon) == True)[0][0]
    
    polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                data[startRange:endRange, 1], 2))
    #p.plot(data[:,0], data[:, 1], data[:,0], polynom(data[:,0]))
    #p.show()
    roots = polynom.r
    if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
        return roots[1]
    else:
        return roots[0]


def _findMpp(data):
    
    polynom = np.poly1d(np.polyfit(data[:, 0], -1 * data[:, 0] * data[:, 1], 3))
    rootsOfDerivitive = polynom.deriv().r
    possibleMax = rootsOfDerivitive[(rootsOfDerivitive > 0) & (rootsOfDerivitive < 1)]
    if possibleMax.size > 1:
        logging.info('Found more than one possible Mpp: ' + str(possibleMax))
    
    returnArray = np.empty([possibleMax.size,2])
    for i in range(0, possibleMax.size):
        returnArray[i, :] = possibleMax[i],polynom(possibleMax[i])
    return returnArray


def _findRs(data):
    indexRange = 5 # Size of range around U = 0 that will be sampled for linear fit
    
    firstPositiveVoltage = np.where((data[:, 0] > 0) == True)[0][0]
    fitRange = range(firstPositiveVoltage-indexRange, firstPositiveVoltage+indexRange)

    return np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]


def _findRp(data):
    indexRange = 5 # Size of range around U = 0 that will be sampled for linear fit
    
    firstPositiveCurrent = np.where((data[:, 1] > 0) == True)[0][0]
    fitRange = range(firstPositiveCurrent-indexRange, firstPositiveCurrent+indexRange)

    return np.polyfit(data[fitRange, 0], data[fitRange, 1], 1)[0]


def evaluateLightData(data, area):
    '''
        Expects an array where each entry contains a U and I data point.
    '''
    
    Isc = _findIsc(data)
    Voc = _findVoc(data)
    jsc = Isc / area
    MppPoint = _findMpp(data)[0]
    FF = -1 * MppPoint[1] / (Voc * Isc)
    
    Rs = _findRs(data)
    Rp = _findRp(data)
    
   
    return Voc, Isc, FF, MppPoint, jsc , Rs, Rp
   
        
        
        

def evaluateUIData(data):
    '''
        Expects an array where each entry contains a U and I data point.
    '''
    
    
    
    print(data)


 
