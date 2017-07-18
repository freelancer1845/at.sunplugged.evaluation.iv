'''
Created on 18.07.2017

@author: jasch
'''

class CellDataObject():
    '''
    Object representation of CellData
    '''
    stringRepFormat = 'DataObject --- Id:"{}" Name:"{}" Description:"{}" Voc:"{}" Isc:"{}" FF:"{}" Jsc:"{}" Rp:"{}" Rs:"{}" Eff:"{}"'

    def __init__(self):
        '''
        Constructor
        '''
        self.Id = None
        self.Name = None
        self.Description = None
        self.Voc = None
        self.Isc = None
        self.FF = None
        self.Jsc = None
        self.Rp = None
        self.Rs = None
        self.Eff = None
        self.data = None
        
    def __str__(self):
        return self.stringRepFormat.format(self.Id, self.Name, self.Description, self.Voc, self.Isc, self.FF, self.Jsc, self.Rp, self.Rs, self.Eff)