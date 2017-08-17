'''
Created on 18.07.2017

@author: Jascha Riedel
'''

from evaluation.lightevaluation import *
import matplotlib.pyplot as plt


class CellDataObject():
    '''
    Object representation of CellData
    
    Attributes:
        Id: Unique Identifier of the data linking it to a specific probe
        Voc: ...
        Isc: ...
        FF: Fill Factor
        Jsc: Isc / Area
        Rp: Shunt Resistance 
        Rs: Series Resistance
        Eff: Efficiency
        Mpp: Maximum Power
        Area: Area of the cell
        data: 2-D Array containing U-I data
    '''
    stringRepFormat = 'DataObject --- Id:"{}" Voc:"{}" Isc:"{}" FF:"{}" Jsc:"{}" Rp:"{}" Rs:"{}" Eff:"{}"'

    def __init__(self):
        '''
        Constructor
        '''
        self.Id = None
        self.Voc = None
        self.Isc = None
        self.FF = None
        self.Rp = None
        self.Rs = None
        self.Eff = None
        self.MppU = None
        self.MppI = None
        self.Area = None
        self.powerInput = None
        self.data = None
        
    @property
    def Id(self):
        return self.__Id;
    
    @Id.setter
    def Id(self, Id):
        self.__Id = str(Id)
    
    
    @property
    def Jsc(self):
        if self.Isc is not None and self.Area is not None:
            return abs(self.Isc) / self.Area
        else:
            return None
        
    @property
    def MppA(self):
        if self.MppU != None and self.MppI != None and self.Area is not None:
            return self.Mpp / self.Area
        else:
            return None
    
    @property
    def Mpp(self):
        if self.MppU != None and self.MppI != None:
            return abs(self.MppI * self.MppU)
        else:
            return None

        
    @staticmethod
    def createFromData(Id, data, area = None, powerInput = None):
        """
        Creates a CellDataObject from U-I Data [V, A], area[cm^2] and powerInput[W]
        area and powerInput are required for Efficiency
        """
        cellDataObject = CellDataObject()
        cellDataObject.data = data
        cellDataObject.Id = Id
        cellDataObject.Voc = findVoc(data)
        cellDataObject.Isc = findIsc(data)
        mppResult = findMpp(data)
        cellDataObject.MppU = mppResult[0]
        cellDataObject.MppI = mppResult[1]
        cellDataObject.Rs = findRp(data)
        cellDataObject.Rp = findRs(data)
        cellDataObject.FF = calculateFF(cellDataObject.Voc, cellDataObject.Isc, cellDataObject.Mpp)
        if area != None:
            cellDataObject.Area = area
        if area != None and powerInput != None:
            cellDataObject.Eff = calculateEff(cellDataObject.Mpp / area, powerInput)
            cellDataObject.powerInput = powerInput

        return cellDataObject
        
    def plotCellDataObject(self):
        if isinstance(self, CellDataObject) is False:
            raise ValueError("Only CellDataObjects allowed!")
        
        
        ymin = min(self.data[:,1]) - 0.1 * abs(min(self.data[:,1]))
        ymax = max(self.data[:,1]) + 0.1 * abs(max(self.data[:,1]))
        data = self.data
        
        plt.plot(data[:,0], data[:,1], label="U-I Data")
        plt.plot(data[:,0], data[:,0] * data[:,1], label="Power")
        if self.Isc is not None and self.Rp is not None:
                plt.plot(self.data[:,0], 1 / self.Rp * self.data[:,0] + self.Isc, label='RP')
                plt.plot(0, self.Isc, 'x', label='Isc', zorder=200)
        if self.Voc is not None and self.Rs is not None:
            plt.plot(self.data[:,0], 1 / self.Rs * self.data[:,0] - self.Voc *  1 / self.Rs, label='RS')
            plt.plot(self.Voc, 0, 'x', label='Voc', zorder=200)
        
        if self.Mpp is not None:
            plt.plot(self.MppU, self.Mpp, 'x', label = 'Mpp', zorder=200)
            if self.Mpp > ymax:
                ymax = self.Mpp * 1.1
        
        #plt.set_ylim(ymin, ymax)
        #plt.set_xlabel('U')
        #plt.set_ylabel('I')
        #plt.set_title(self.Id)
        plt.grid()
        plt.legend(fontsize=6)
        plt.axhline(y=0, color='k')
        plt.axvline(x=0, color='k')
        
        plt.show()

    def __str__(self):
        return self.stringRepFormat.format(self.Id, self.Voc, self.Isc, self.FF, self.Jsc, self.Rp, self.Rs, self.Eff)
    
    



    
    
    

    