'''
Created on 21.07.2017

@author: Jascha Riedel
'''


def calculateFF(Voc, Isc, Mpp):
    '''
    Calculates the FillFactor from Voc Isc and Mpp
    '''
    return abs(Mpp / Voc / Isc * 100)