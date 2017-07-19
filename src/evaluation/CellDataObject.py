'''
Created on 18.07.2017

@author: Jascha Riedel
'''



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
        self.Mpp = None
        self.Area = None
        self.data = None
        
    
    @property
    def Jsc(self):
        if self.Isc is not None and self.Area is not None:
            return abs(self.Isc) / self.Area
        else:
            return None;
        
    @property
    def MppA(self):
        if self.Mpp is not None and self.Area is not None:
            return self.Mpp / self.Area
        else:
            return None;
    
    def __str__(self):
        return self.stringRepFormat.format(self.Id, self.Voc, self.Isc, self.FF, self.Jsc, self.Rp, self.Rs, self.Eff)
    
    