'''
Created on 21.07.2017

@author: Jascha Riedel
'''

"""
def calculateEff(Voc, Isc, FF, Pin):
    '''
    Calculates the Efficiency from Voc, Isc, FF and PowerIn (light source power)
    '''
    return abs(Voc * Isc * FF / Pin) * 100
"""
def calculateEff(Mpp, Pin):
    '''
    Calculates the Efficiency from Maximum Powerpoint and PowerIn (light source power)
    '''
    return abs(Mpp / Pin) * 10000 * 100