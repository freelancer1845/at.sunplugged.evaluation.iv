'''
Created on 13.07.2017

@author: Jascha Riedel
'''

import openpyxl
from openpyxl.utils import get_column_letter
from evaluation.CellDataObject import CellDataObject
from formattedOutput.ResultsSheet import fillResultsSheet
from formattedOutput.CellDataObjectSheet import createCellDataObjectSheet

SHEET_DATA_TITLE = "DataSheet"
SHEET_RESULTS_TITLE = "Results"
SHEET_DATA_PREFIX = "Data-"


def _createWorkbook(excelFile):
    wb = openpyxl.Workbook()
    wb.active.title = SHEET_RESULTS_TITLE
    
    return wb





def saveCellDataObjects(excelFile, cellDataObjects):
    if isinstance(cellDataObjects, (list, tuple)) is True:
        for dataObject in cellDataObjects:
            if isinstance(dataObject, CellDataObject) is False:
                raise ValueError('Can only process CellDataObjects!')
    else:
        raise ValueError('Parameter cellDataObjects must be list or tuple!')
    
    if isinstance(excelFile, str) is False:
        raise ValueError('Parameter excelFile must be str!')
    
    wb = _createWorkbook(excelFile)
    fillResultsSheet(wb.get_sheet_by_name(SHEET_RESULTS_TITLE), cellDataObjects)
    for idx,cellDataObject in enumerate(cellDataObjects, start = 2):
        sheet = wb.create_sheet(SHEET_DATA_PREFIX + str(cellDataObject.Id), idx)
        createCellDataObjectSheet(sheet, cellDataObject)

    
    wb.save(excelFile)

def _createDataSheet(_sheet, dataObjects):
    currentColumn = 1
    for dataObject in dataObjects:
        _sheet.column_dimensions[get_column_letter(currentColumn)].width = 20
        _sheet.column_dimensions[get_column_letter(currentColumn + 1)].width = 20
        
        nameCellX = _sheet.cell(row = 1, column = currentColumn)
        nameCellY = _sheet.cell(row = 1, column = currentColumn + 1)
        nameCellX.value = 'U-' + dataObject.texName
        nameCellY.value = 'I-' + dataObject.texName
        
        data = dataObject.data;
        currentRow = 2
        for point in data:
            _sheet.cell(row = currentRow, column = currentColumn).value = point[0]
            _sheet.cell(row = currentRow, column = currentColumn + 1).value = point[1]
            currentRow +=1
    
        currentColumn += 2


def _createResultsSheet(sheet, dataObjects, attribs):
    sheet.cell(row = 1, column = 1).value = 'Sample Name'
    currentColumn = 2
    for attrib in attribs:
        sheet.cell(row = 1, column = currentColumn).value = attrib
        currentColumn +=1
    
    currentRow = 2
    for dataObject in dataObjects:
        sheet.cell(row = currentRow, column = 1).value = dataObject.texName
        sheet.column_dimensions[get_column_letter(1)].width = 20
        currentColumn = 2
        for attrib in attribs:
            sheet.column_dimensions[get_column_letter(currentColumn)].width = 20
            
            value = getattr(dataObject, attrib)
            if value is None:
                value = "#NUM!"
            sheet.cell(row = currentRow, column = currentColumn).value = value
            currentColumn += 1
        
        currentRow += 1
    
    

def writeDataToExcelFile(excelFile, dataObjects, attribs):
    wb = openpyxl.Workbook()
    wb.active.title = SHEET_DATA_TITLE
    
    wb.create_sheet(title = SHEET_RESULTS_TITLE)
    
    _createDataSheet(wb.get_sheet_by_name(SHEET_DATA_TITLE), dataObjects)
    _createResultsSheet(wb.get_sheet_by_name(SHEET_RESULTS_TITLE), dataObjects, attribs)
    
    
    wb.save(excelFile)
