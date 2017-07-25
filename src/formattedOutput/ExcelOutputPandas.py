'''
Created on 25.07.2017

@author: Jascha Riedel
'''

import pandas as pd
from evaluation import CellDataObject
from formattedOutput.CellDataObjectSheetPandas import createCellDataSheet
from formattedOutput.ResultsSheetPandas import createResultsSheet

def saveCellDataObjects(excelFile, cellDataObjects):
    if isinstance(cellDataObjects, (list, tuple)) is True:
        for dataObject in cellDataObjects:
            if isinstance(dataObject, CellDataObject) is False:
                raise ValueError('Can only process CellDataObjects!')
    else:
        raise ValueError('Parameter cellDataObjects must be list or tuple!')
    
    if isinstance(excelFile, str) is False:
        raise ValueError('Parameter excelFile must be str!')
    
    engines = ['xlwt', 'xlsxwriter']
    
    if excelFile.endswith('.xls'):
        print('Info: Charts are not supported for Excel 2003 Output format...')
        writer = pd.ExcelWriter(excelFile, engine=engines[0])
    else:
        writer = pd.ExcelWriter(excelFile, engine=engines[1])
    
    createResultsSheet(writer, cellDataObjects)
    for cellDataObject in cellDataObjects:
        createCellDataSheet(writer, cellDataObject)
    
    writer.save()
        
