'''
Created on 18.07.2017

@author: Jascha Riedel
'''

import pyodbc
from evaluation.CellDataObject import CellDataObject

connStrFormat = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ="
)



    
    



class DatabaseConnection():
    '''
    Initialized with the SPROD Microsoft Access database file you can data records by refered to by their id.
    '''

    def __init__(self, databaseFile):
        '''
        Constructor
        '''
        self._openDatabseConnection(databaseFile)
    
    
    def getDatabaseEntries(self, ids):
        mesRows = self._getMesRows(ids)
        cellDataObjects = []
        for mes in mesRows:
            data = self._createDataObjectFromMesRow(mes)
            cellDataObjects.append(data)
        
        return cellDataObjects
    
    
    def _createDataObjectFromMesRow(self, mes):
        dataObject = CellDataObject()
        dataObject.Id = mes[0]
        results = self._getResults(mes)
        dataObject.Voc = results[0]
        dataObject.Isc = results[1]
        dataObject.FF = results[2]
        dataObject.Eff = results[3]
        dataObject.Rp = results[4]
        dataObject.Rs = results[5]
        return dataObject
    
    def _getResults(self, mes):
        sql = 'SELECT RsVoc,RsIsc,RsMxe,RsEff,RsRsr,RsRsh FROM MesRes WHERE ID={}'.format(mes[1])
        return self._executeAndFetchAll(sql)[0]
        
        
        
    
    def _getMesRows(self, ids):
        sql = 'SELECT Id,ResId,CelId,Mid,DtCr FROM Mes WHERE ID IN('
        first = True
        for mesId in ids:
            if first is False:
                sql += ','
            else:
                first = False
            sql += str(mesId)
        
        sql += ')'
        return self._executeAndFetchAll(sql)
    
    def _executeAndFetchAll(self, sql):
        print('Executing SQL and Fetchall for Sql:"{}"'.format(sql))
        crsr = self.connection.cursor()
        res = crsr.execute(sql)
        rows = res.fetchall()
        crsr.close()
        return rows
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._cleanUp()
    
    def _openDatabseConnection(self, databaseFile):
        connStr = connStrFormat + databaseFile + ";"
        self.connection = pyodbc.connect(connStr)
        print('successfully connected')
    
    def _cleanUp(self):
        if self.connection is not None:
            self.connection.close()
            print('Closed SQL Access connection...')
        
        print('Successfully finished Database Connection...')




if __name__ == '__main__':
    with DatabaseConnection("C:\\Users\\jasch\\SunpluggedJob\\SPROD\\SPROD.mdb") as db:
        print('Connected')
        db.getDatabaseEntries([556,557])
        print('Done')