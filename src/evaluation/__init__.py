'''
Created on Jul 1, 2017

@author: Jascha Riedel
'''

import numpy
from scipy import stats

def evaluateUIData(data):
    '''
        Expects an array where each entry contains a U and I data point.
    '''
    
    
    
    print(data)


def evaluateLightData(data, area):
    '''
        Expects an array where each entry contains a U and I data point.
    '''
    voltage = []
    current = []
    for pair in data:
        voltage.append(pair[0])
        current.append(pair[1])
    print(voltage)
    print(current)
    I1 = max([elem for elem in current if elem<0])
    V1 = max([elem for elem in voltage if elem<0])
    posV = [i for i,x in enumerate(current) if x==I1]
    posI = [i for i,x in enumerate(voltage) if x==V1]
    Isc = (current[posI[0]]+current[posI[0]+1])/2
    jsc = Isc/area
    Voc = (voltage[posV[0]]+voltage[posV[0]+1])/2
    Mpp = max(-1*numpy.array(current)*numpy.array(voltage))
    FF = -1*Mpp/(Voc*Isc)
    a=5
    #Data for light\n",
    selectData =voltage[posV[0]-a:posV[0]+a],current[posV[0]-a:posV[0]+a]#data for fitting Rs \n",
    selectDataRp =voltage[posI[0]-a:posI[0]+a],current[posI[0]-a:posI[0]+a]#data for fitting Rp\n",
    #Regressions\n",
    slopeRS, interceptRS, r_value, p_value, std_err = stats.linregress(selectData[0],selectData[1])
    slopeRp, interceptRp, r_value, p_value, std_err = stats.linregress(selectDataRp[0],selectDataRp[1])
    return Voc,Isc,FF,Mpp,jsc ,selectData,slopeRS, interceptRS,slopeRp, interceptRp
    