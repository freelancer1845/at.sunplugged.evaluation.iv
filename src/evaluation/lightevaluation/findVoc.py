'''
Created on 21.07.2017

@author: Jascha Riedel
'''

import numpy as np

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
        return findVoc(data, epsilon * 10)
    
    polynom = np.poly1d(np.polyfit(data[startRange:endRange, 0],
                data[startRange:endRange, 1], 1))
    #p.plot(data[:,0], data[:, 1], data[:,0], polynom(data[:,0]))
    #p.show()
    roots = polynom.r
    if roots[0] < data[0,0] or roots[0] > data[data[:,0].size-1,0]:
        return roots[1]
    else:
        return roots[0]
