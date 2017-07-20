'''
Created on 18.07.2017

@author: Jascha Riedel
'''

from evaluation import LightEvaluation

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

    def __str__(self):
        return self.stringRepFormat.format(self.Id, self.Voc, self.Isc, self.FF, self.Jsc, self.Rp, self.Rs, self.Eff)
    
    